// -*- coding: utf-8 -*-
//
//  mrsimulator.h
//
//  @copyright Deepansh J. Srivastava, 2019-2020.
//  Created by Deepansh J. Srivastava, Jun 30, 2019
//  Contact email = deepansh2012@gmail.com
//

#ifndef mrsimulator_h
#define mrsimulator_h

#include "angular_momentum.h"
#include "config.h"
#include "fftw3.h"
#include "frequency_tensor.h"
#include "isotopomer_ravel.h"
#include "schemes.h"

/**
 * @struct MRS_plan
 * An mrsimulator plan for computing lineshapes lineshape. An mrsimulator plan,
 * MRS_plan includes,
 *    - a pre-calculated MRS_averaging_scheme.
 *    - pre-calculating stacked arrays of irreducible second rank,
 * wigner-2j(β), and fourth rank, wigner-4j(β), matrices at every
 * orientation angle β,
 *    - pre-calculating the exponent of the sideband order phase,
 *      @f$\exp(-im\alpha)@f$, at every orientation angle α,
 *    - creating the fftw plan, and
 *    - allocating buffer for storing the evaluated frequencies and their
 *      respective amplitudes.
 *
 * Creating a plan adds an overhead to the lineshape simulation. We suggest
 * creating a plan at the start and re-using it as necessary. This is
 * especially efficient when performing a batch simulation, such as,
 * simulating lineshapes from thousands of sites.
 */

struct MRS_plan {
  /**
   * A pointer to the MRS_averaging_scheme orientation averaging scheme.
   */
  MRS_averaging_scheme *averaging_scheme;

  int number_of_sidebands; /**< The number of sidebands to compute. */

  double sample_rotation_frequency_in_Hz; /**< The sample rotation frequency in
                                             Hz. */

  /**
   * The angle, in radians, describing the sample axis-rotation with respect to
   * the lab-frame z-axis.
   */
  double rotor_angle_in_rad;

  /** \privatesection */
  /**
   * The sideband frequency ratio stored in the fft output order. The sideband
   * frequency ratio is defined as the ratio -
   *    @f[\frac{n \omega_r}{n_i}@f]
   * where `n` is an integer, @f$\omega_r@f$ is the spinning frequency frequency
   * in Hz, and @f$n_i@f$ is the `increment` along the spectroscopic grid
   * dimension.
   */
  double *vr_freq;

  /** The isotropic frequency offset ratio. The ratio is similarly defined as
   * before. */
  double isotropic_offset;

  /** The buffer to hold the sideband amplitudes as stride 2 array after
   * mrsimulator processing.
   */

  bool allow_fourth_rank;   // If true, creates buffer and tables for processing
                            // fourth rank tensors.
  unsigned int size;        //  number of orientations * number of sizebands.
  unsigned int n_octants;   //  number of octants used in the simulation.
  double *norm_amplitudes;  //  array of normalized amplitudes per orientation.
  double *wigner_d2m0_vector;  //  wigner-2j dm0 vector, n ∈ [-2, 2].
  double *wigner_d4m0_vector;  //  wigner-4j dm0 vector, n ∈ [-4, 4].
  complex128 *pre_phase;    //  generic buffer for sideband phase calculation.
  complex128 *pre_phase_2;  //  buffer for 2nk rank sideband phase calculation.
  complex128 *pre_phase_4;  //  buffer for 4th rank sideband phase calculation.
  complex128 one;           //  holds complex value 1.
  complex128 zero;          //  hold complex value 0.
  double buffer;            //  buffer for temporary storage.
};

typedef struct MRS_plan MRS_plan;

/**
 * Create a new mrsimulator plan.
 *
 * @param	scheme The MRS_averaging_scheme.
 * @param number_of_sidebands The number of sideband to compute.
 * @param sample_rotation_frequency_in_Hz The sample rotation frequency in Hz.
 * @param rotor_angle_in_rad The polar angle in radians with respect to z-axis
 *            describing the axis of rotation.
 * @param increment The increment along the spectroscopic dimension.
 * @param allow_fourth_rank When true, the plan calculates matrices for
 *            processing the fourth rank tensor.
 * @return A pointer to the MRS_plan.
 */
MRS_plan *MRS_create_plan(MRS_averaging_scheme *scheme, int number_of_sidebands,
                          double sample_rotation_frequency_in_Hz,
                          double rotor_angle_in_rad, double increment,
                          bool allow_fourth_rank);

/**
 * @brief Release the memory allocated for the given mrsimulator plan.
 *
 * @param	plan The pointer to the MRS_plan.
 */
void MRS_free_plan(MRS_plan *plan);

/* Update the MRS plan when sample rotation frequency change. */
void MRS_plan_update_from_sample_rotation_frequency_in_Hz(
    MRS_plan *plan, double increment, double sample_rotation_frequency_in_Hz);

/* Update the MRS plan when the rotor angle chaange. */
void MRS_plan_update_from_rotor_angle_in_rad(MRS_plan *plan,
                                             double rotor_angle_in_rad,
                                             bool allow_fourth_rank);

/**
 * Free the memory from the mrsimulator plan associated with the wigner
 * d^l_{m,0}(rotor_angle_in_rad) vectors. Here, l=2 or 4.
 */
void MRS_plan_free_rotor_angle_in_rad(MRS_plan *plan);

/**
 * @brief Return a copy of the mrsimulator plan.
 *
 * @param plan The pointer to the plan to be copied.
 * @return MRS_plan = A pointer to the copied plan.
 * This function is incomplete.
 */
MRS_plan *MRS_copy_plan(MRS_plan *plan);

/**
 * @brief Process the plan for the amplitudes at every orientation.
 *
 * The method takes the arguments @p R2 and @p R4 vectors defined in a crystal /
 * commmon frame and evaluates the amplitudes corresponding to the @p R2 and @p
 * R4 vectors in the lab frame. The transformation from the crystal / commmon
 * frame to the lab frame is done using the wigner 2j and 4j rotation matrices
 * over all orientations. The sideband amplitudes are evaluated using equation
 * [39] of the reference https://doi.org/10.1006/jmre.1998.1427.
 *
 * @param scheme The pointer to the powder averaging scheme of type
 *            MRS_averaging_scheme.
 * @param	plan A pointer to the mrsimulator plan of type MRS_plan.
 * @param fftw_scheme A pointer to the fftw scheme of type MRS_fftw_scheme.
 * @param refresh If true, zero the result array `vector` before proceeding,
 *            else update the result.
 */
void MRS_get_amplitudes_from_plan(MRS_averaging_scheme *scheme, MRS_plan *plan,
                                  MRS_fftw_scheme *fftw_scheme, bool refresh);

/**
 * @brief Process the plan for normalized frequencies at every orientation.
 *
 * @param scheme The pointer to the powder averaging scheme of type
 *            MRS_averaging_scheme.
 * @param	plan A pointer to the mrsimulator plan of type MRS_plan.
 * @param	R0 The irreducible zeroth rank frequency component.
 * @param R2 A pointer to the product of the spatial coefficients and the spin
 *            transition functions of the second rank tensor. The vector
 *            @p R2 is a complex128 array of length 5 with the first element
 *            corresponding to the product of the spin transition function and
 *            the coefficient of the @f$T_{2,-2}@f$ spatial irreducible tensor.
 * @param R4 A pointer to the product of the spatial part coefficients of the
 *            fourth rank tensor and the spin transition functions. The vector
 *            @p R4 is a complex128 array of length 9 with the first element
 *            corresponding to the product of the spin transition function and
 *            the coefficient of the @f$T_{4,-4}@f$ spatial irreducible tensor.
 * @param refresh If true, zero the frequencies before update, else self update.
 * @param normalize_offset
 * @param inverse_increment The inverse of the increment along the dimension
 *            (sequence).
 */
void MRS_get_normalized_frequencies_from_plan(MRS_averaging_scheme *scheme,
                                              MRS_plan *plan, double R0,
                                              complex128 *R2, complex128 *R4,
                                              bool refresh,
                                              double normalize_offset,
                                              double inverse_increment);

void MRS_get_frequencies_from_plan(MRS_averaging_scheme *scheme, MRS_plan *plan,
                                   double R0, complex128 *R2, complex128 *R4,
                                   bool refresh);

/**
 * @func MRS_rotate_components_from_PAS_to_common_frame
 *
 * The function evaluates the tensor components from the principal axis system
 * (PAS) to the common frame of the isotopomer.
 *
 * @param ravel_isotopomer A pointer to the isotopomer_ravel structure.
 * @param transition A pointer to the spin quantum numbers from the inital and
 *        final states of the spin transition packed as initial quantum numbers
 *        followed by the final quantum numbers.
 * @param allow_fourth_rank A boolean, if true, also evalute the frequency
 *        contributions from the fourth rank tensor.
 * @param R0 A pointer to location where the frequency contributions from the
 *        zeroth rank tensor is stored.
 * @param R2 A pointer to location where the frequency contributions from the
 *        second rank tensor is stored.
 * @param R4 A pointer to location where the frequency contributions from the
 *        fourth rank tensor is stored.
 * @param R0_temp A pointer to location where the frequency contributions from
 *        the zeroth rank tensor is temporarily stored.
 * @param R2_temp A pointer to location where the frequency contributions from
 *        the second rank tensor is temporarily stored.
 * @param R4_temp A pointer to location where the frequency contributions from
 *        the fourth rank tensor is temporarily stored.
 * @param remove_2nd_order_quad_isotropic A boolean, if true, remove the
 *        isotropic contribution from the fourth rank tensor.
 * @param B0_in_T The magnetic flux density of the macroscopic external magnetic
 *        field in units of T.
 */
void MRS_rotate_components_from_PAS_to_common_frame(
    isotopomer_ravel *ravel_isotopomer,  // isotopomer structure
    float *transition,                   // the pointer to the spin transition.
    bool allow_fourth_rank,  // if true, pre for 4th rank computation
    double *R0,              // the R0 components
    complex128 *R2,          // the R2 components
    complex128 *R4,          // the R4 components
    double *R0_temp,         // the temporary R0 components
    complex128 *R2_temp,     // the temporary R2 components
    complex128 *R4_temp,     // the temporary R3 components
    bool remove_2nd_order_quad_isotropic,  // if true, remove 2nd order quad
                                           // isotropic shift
    double B0_in_T);

extern void __get_components(int number_of_sidebands, double spin_frequency,
                             double *restrict pre_phase);

#endif /* mrsimulator_h */
