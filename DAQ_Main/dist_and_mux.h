/*dis_and_mux.h
 *Created by:   Joshua Chapman
 *Date:         11/15/2023
 *Description:  This file contains code for interfacing with the VL53L4CX through a PCA9548 I2C Mux. It is intended to allow for several sensors to operate in parallel.
 *Version:      0.0 - This code is still under development.
*/

#include <Arduino.h>
#include <Wire.h>

//Distance Sensor Libraries
#include <vl53l4cx_class.h>
#include <vl53l4cx_def.h>
#include <vl53l4cx_dmax_private_structs.h>
#include <vl53l4cx_dmax_structs.h>
#include <vl53l4cx_error_codes.h>
#include <vl53l4cx_error_exceptions.h>
#include <vl53l4cx_hist_map.h>
#include <vl53l4cx_hist_private_structs.h>
#include <vl53l4cx_hist_structs.h>
#include <vl53l4cx_ll_def.h>
#include <vl53l4cx_ll_device.h>
#include <vl53l4cx_nvm_map.h>
#include <vl53l4cx_nvm_structs.h>
#include <vl53l4cx_platform_user_config.h>
#include <vl53l4cx_platform_user_data.h>
#include <vl53l4cx_platform_user_defines.h>
#include <vl53l4cx_preset_setup.h>
#include <vl53l4cx_register_map.h>
#include <vl53l4cx_register_settings.h>
#include <vl53l4cx_register_structs.h>
#include <vl53l4cx_tuning_parm_defaults.h>
#include <vl53l4cx_types.h>
#include <vl53l4cx_xtalk_private_structs.h>


#define DEV_I2C Wire


#define dist_address_write 0x52
#define Model_ID_address = 0x010F
#define Model_ID_Value = 0xEB 

#include <Arduino.h>
#include <Wire.h>
#include <vl53l4cx_class.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <stdlib.h>

#define DEV_I2C Wire
#define SerialPort Serial

#ifndef LED_BUILTIN
  #define LED_BUILTIN 13
#endif
#define LedPin LED_BUILTIN

// Components.
VL53L4CX sensor_vl53l4cx_sat(&DEV_I2C, A1);

/* Setup ---------------------------------------------------------------------*/


class dist_mux{
  public:
  //Constructor
  dist_mux::dist_mux(int mux_index){
    Wire.begin();
    dist_mux::index = mux_index;
    dist_mux::set_index();
    // dist_mux::sensor.begin();
    
    }
    

  void dist_mux::start_read(){
    dist_mux::set_index(); //Set the multiplexor to the correct index
    
    
  }
    

  private:
  //Distance Sensor Class
  VL53L4CX sensor_vl53l4cx_sat(&DEV_I2C, A1);
  // VL53L4CX dist_mux::sensor(Wire, 2); //The pin number here will be a dead pin.
  void dist_mux::set_index(){
    Wire.beginTransmission(0x70); //Talk to MUX
    Wire.write(dist_mux::index);
    Wire.endTransmission();
  }
  int dist_mux::index = 0;

};