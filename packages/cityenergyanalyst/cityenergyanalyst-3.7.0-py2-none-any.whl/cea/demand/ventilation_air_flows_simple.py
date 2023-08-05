# -*- coding: utf-8 -*-


from __future__ import division
import numpy as np
from cea.demand import control_ventilation_systems, constants, control_heating_cooling_systems
from cea.utilities import physics
from cea.constants import HOURS_IN_YEAR

__author__ = "Gabriel Happle"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


# THIS SCRIPT IS USED TO CALCULATE ALL VENTILATION PROPERTIES (AIR FLOWS AND THEIR TEMPERATURES)
# FOR CALCULATION OF THE VENTILATION HEAT TRANSFER H_VE USED IN THE ISO 13790 CALCULATION PROCEDURE

# get values of global variables
ETA_REC = constants.ETA_REC  # constant efficiency of Heat recovery
DELTA_P_DIM = constants.DELTA_P_DIM
H_F = constants.H_F


def calc_air_mass_flow_mechanical_ventilation(bpr, tsd, t):
    """
    Calculates mass flow rate of mechanical ventilation at time step t according to ventilation control options and
     building systems properties

    Author: Gabriel Happle
    Date: 01/2017

    :param bpr: Building properties row object
    :type bpr: cea.demand.thermal_loads.BuildingPropertiesRow
    :param tsd: Timestep data
    :type tsd: Dict[str, numpy.ndarray]
    :param t: time step [0..HOURS_IN_YEAR]
    :type t: int
    :return: updates tsd
    """

    # if has mechanical ventilation and not night flushing : m_ve_mech = m_ve_schedule
    if control_ventilation_systems.is_mechanical_ventilation_active(bpr, tsd, t) \
            and not control_ventilation_systems.is_night_flushing_active(bpr, tsd, t)\
            and not control_ventilation_systems.is_economizer_active(bpr, tsd, t):

        # mechanical ventilation fulfills requirement - ventilation provided by infiltration (similar to CO2 sensor)

        m_ve_mech = max(tsd['m_ve_required'][t] - tsd['m_ve_inf'][t], 0)
        # TODO: check mech ventilation rule - maybe: required + infiltration

    elif control_ventilation_systems.has_mechanical_ventilation(bpr) \
            and control_ventilation_systems.is_night_flushing_active(bpr, tsd, t):

        # night flushing according to strategy
        # ventilation with maximum capacity = maximum required ventilation rate
        m_ve_mech = tsd['m_ve_required'].max()  # TODO: some night flushing rule

    elif control_ventilation_systems.has_mechanical_ventilation(bpr) \
            and control_ventilation_systems.is_economizer_active(bpr, tsd, t):

        # economizer according to strategy
        # ventilation with maximum capacity = maximum required ventilation rate
        m_ve_mech = tsd['m_ve_required'].max()

    elif not control_ventilation_systems.is_mechanical_ventilation_active(bpr, tsd, t):

        # mechanical ventilation is turned off
        m_ve_mech = 0

    else:
        raise ValueError

    tsd['m_ve_mech'][t] = m_ve_mech

    return


def calc_air_mass_flow_window_ventilation(bpr, tsd, t):
    """
    Calculates mass flow rate of window ventilation at time step t according to ventilation control options and
     building systems properties

    Author: Gabriel Happle
    Date: 01/2017

    :param bpr: Building properties row object
    :type bpr: cea.demand.thermal_loads.BuildingPropertiesRow
    :param tsd: Timestep data
    :type tsd: Dict[str, numpy.ndarray]
    :param t: time step [0..HOURS_IN_YEAR]
    :type t: int
    :return: updates tsd
    """

    # if has window ventilation and not special control : m_ve_window = m_ve_schedule
    if control_ventilation_systems.is_window_ventilation_active(bpr, tsd, t) \
            and not control_ventilation_systems.is_night_flushing_active(bpr, tsd, t):

        # window ventilation fulfills requirement (control by occupants similar to CO2 sensor)
        m_ve_window = max(tsd['m_ve_required'][t] - tsd['m_ve_inf'][t], 0)
        # TODO: check window ventilation calculation, there are some methods in SIA2044

    elif control_ventilation_systems.is_window_ventilation_active(bpr, tsd, t) \
            and control_ventilation_systems.is_night_flushing_active(bpr, tsd, t):

        # ventilation with maximum capacity = maximum required ventilation rate
        m_ve_window = max(tsd['m_ve_required'])  # TODO: implement some night flushing rule

    elif not control_ventilation_systems.is_window_ventilation_active(bpr, tsd, t):

        m_ve_window = 0

    else:
        raise ValueError

    tsd['m_ve_window'][t] = m_ve_window

    return


def calc_m_ve_leakage_simple(bpr, tsd):
    """
    Calculates mass flow rate of leakage at time step t according to ventilation control options and
     building systems properties

    Estimation of infiltration air volume flow rate according to Eq. (3) in DIN 1946-6

    Author: Gabriel Happle
    Date: 01/2017

    :param bpr: Building properties row object
    :type bpr: cea.demand.thermal_loads.BuildingPropertiesRow
    :param tsd: Timestep data
    :type tsd: Dict[str, numpy.ndarray]
    :return: updates tsd
    """

    # 'flat rate' infiltration considered for all buildings

    # get properties
    n50 = bpr.architecture.n50
    area_f = bpr.rc_model['Af']

    # estimation of infiltration air volume flow rate according to Eq. (3) in DIN 1946-6
    n_inf = 0.5 * n50 * (DELTA_P_DIM / 50) ** (2 / 3)  # [air changes per hour] m3/h.m2
    infiltration = H_F * area_f * n_inf * 0.000277778  # m3/s

    tsd['m_ve_inf'] = infiltration * physics.calc_rho_air(tsd['T_ext'][:])  # (kg/s)

    return


def calc_theta_ve_mech(bpr, tsd, t):
    """
    Calculates supply temperature of mechanical ventilation system according to ventilation control options and
     building systems properties

    Author: Gabriel Happle
    Date: 01/2017

    :param bpr: Building properties row object
    :type bpr: cea.demand.thermal_loads.BuildingPropertiesRow
    :param tsd: Timestep data
    :type tsd: Dict[str, numpy.ndarray]
    :param t: time step [0..HOURS_IN_YEAR]
    :type t: int
    :return: updates tsd
    """

    if control_ventilation_systems.is_mechanical_ventilation_heat_recovery_active(bpr, tsd, t):

        theta_eta_rec = tsd['T_int'][t-1]

        theta_ve_mech = tsd['T_ext'][t] + ETA_REC * (theta_eta_rec - tsd['T_ext'][t])  # TODO: some HEX formula

    # if no heat recovery: theta_ve_mech = theta_ext
    elif not control_ventilation_systems.is_mechanical_ventilation_heat_recovery_active(bpr, tsd, t):

        theta_ve_mech = tsd['T_ext'][t]

    else:

        theta_ve_mech = np.nan
        print('Warning! Unknown HEX  status')

    tsd['theta_ve_mech'][t] = theta_ve_mech

    return


def calc_m_ve_required(bpr, tsd):
    """
    Calculate required outdoor air ventilation rate according to occupancy

    Author: Legacy
    Date: old

    :param tsd: Timestep data
    :type tsd: Dict[str, numpy.ndarray]
    :return: updates tsd
    """

    m_ve_required_people = (tsd['ve']/3.6) * physics.calc_rho_air(tsd['T_ext'][:]) * 0.001  # kg/s

    if control_heating_cooling_systems.has_3for2_cooling_system(bpr) \
            or control_heating_cooling_systems.has_central_ac_cooling_system(bpr):
        # 0.6 l/s/m2 minimum ventilation rate according to Singapore standard SS 553
        # air conditioning systems supply the higher rate between minimum flow per area and required ventilation for
        #  people during occupied hours. The minimum flow rate ensures dilution of pollutants inside the building
        # This applies to buildings with air-conditioning systems for cooling
        # [https://escholarship.org/content/qt7k1796zv/qt7k1796zv.pdf]
        m_ve_required_min = constants.MIN_VENTILATION_RATE * bpr.rc_model['Af'] * physics.calc_rho_air(tsd['T_ext'][:]) * 0.001  # kg/s
        # we want this not to affect the air flows during the heating season
        m_ve_required = []
        for t in range(0, HOURS_IN_YEAR):
            if 0.0 < m_ve_required_people[t] < m_ve_required_min[t] and \
                control_heating_cooling_systems.is_cooling_season(t, bpr):
                m_ve_required.append(m_ve_required_min[t])
            else:
                m_ve_required.append(m_ve_required_people[t])

        #m_ve_required = [req_min if 0.0 < req_peop < req_min else req_peop for req_min, req_peop in zip(m_ve_required_min, m_ve_required_people)]
        m_ve_required = np.asarray(m_ve_required) # convert list to array

    else:
        m_ve_required = m_ve_required_people

    tsd['m_ve_required'] = m_ve_required

    return
