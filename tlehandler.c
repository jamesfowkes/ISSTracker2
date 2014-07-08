/*
 * tlehandler.c
 *
 *  Provides TLE support for tracker application
 *
 *  Created on: 02 July 2014
 *      Author: james
 *
 *		Target: ATMEGA128
 */

/*
 * Standard Library Includes
 */

#include <stdbool.h>
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

/*
 * Utility Includes
 */

// None

/*
 * AVR Includes (Defines and Primitives)
 */

#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>

/*
 * SGP Library Includes
 */

#include "sgp.h"

/*
 * Utility Library Includes
 */

#include "util_memory_placement.h"
#include "util_earth.h"
#include "util_angle.h"
#include "util_time.h"
#include "util_geo.h"

/*
 * Application Includes
 */

#include "tlehandler.h"

/*
 * Private Defines and Datatypes
 */

#define TLE_TITLE_LENGTH 24
#define TLE_LINE_LENGTH 69

#define DEFAULT_TLE_TITLE "0 ISS (ZARYA)           " // Maximum of 24 chars
#define DEFAULT_TLE_LINE1 "1 25544U 98067A   14135.79915963  .00006959  00000-0  12068-3 0  2984" // Maximum of 69 chars
#define DEFAULT_TLE_LINE2 "2 25544 051.6467 260.1457 0003007 358.3551 001.7946 15.50235663886304" // Maximum of 69 chars

/*
 * Private Function Prototypes
 */
 
static void updateTLEData(void);

/*
 * Private Variables
 */

static char line0[] = DEFAULT_TLE_TITLE; 
static char line1[] = DEFAULT_TLE_LINE1;
static char line2[] = DEFAULT_TLE_LINE2;

char IN_EEPROM(eeprom_line0[]) = DEFAULT_TLE_TITLE;
char IN_EEPROM(eeprom_line1[]) = DEFAULT_TLE_LINE1;
char IN_EEPROM(eeprom_line2[]) = DEFAULT_TLE_LINE2;

struct tle_ascii s_TLE = {
	{line0,
	line1,
	line2}
};

struct sgp_data s_data;

static struct vector pos;

VECTOR_3D s_observer;

/*
 * Public Function Definitions
 */
 
void TLE_Handler_Init(void)
{
	// Read latest TLE from EEPROM
	eeprom_read_block(line0, eeprom_line0, TLE_TITLE_LENGTH);
	eeprom_read_block(line1, eeprom_line1, TLE_LINE_LENGTH);
	eeprom_read_block(line2, eeprom_line2, TLE_LINE_LENGTH);
	
	updateTLEData();
	
}

void TLE_Handler_SetNewTLE(char * l0, char * l1, char * l2)
{
	if (l0 && l1 && l2)
	{
		strncpy(line0, l0, TLE_TITLE_LENGTH);
		strncpy(line1, l1, TLE_LINE_LENGTH);
		strncpy(line2, l2, TLE_LINE_LENGTH);
		
		eeprom_write_block(line0, eeprom_line0, TLE_TITLE_LENGTH);
		eeprom_write_block(line1, eeprom_line1, TLE_LINE_LENGTH);
		eeprom_write_block(line2, eeprom_line2, TLE_LINE_LENGTH);
		
		updateTLEData();
	}
}

void TLE_Handler_Update(TM * time)
{
	double epoch;
	
	int year = time->tm_year;
	while (year > 100) { year -= 100; }
	
	epoch = (double)year * 100.0;
	epoch += time->tm_yday;
	epoch += (double)time->tm_hour / (double)HOURS_PER_DAY;
	epoch += (double)time->tm_min / (double)MINS_PER_DAY;
	epoch += (double)time->tm_sec / (double)S_PER_DAY;
	
	sgp4call(Julian_Date_of_Epoch(epoch), &pos, NULL, &s_data);
	Convert_Sat_State(&pos, NULL);
}

void TLE_Handler_GetViewAngles(VIEW_ANGLES * viewAngles)
{
	VECTOR_3D sat = {(float)pos.v[0], (float)pos.v[1], (float)pos.v[2]};
	
	VECTOR_3D observerToSat;
	Difference_3DVectors(&s_observer, &sat, &observerToSat);
	
	viewAngles->azimuth = Azimuth_3DVector(&observerToSat);
	viewAngles->elevation = Elevation_3DVector(&observerToSat);
}

void TLE_Handler_SetObserverCoords(float x_km, float y_km, float z_km)
{
	s_observer.x = x_km;
	s_observer.y = y_km;
	s_observer.z = z_km;
}

/*
 * Public Function Definitions
 */
 
static void updateTLEData(void)
{
	Convert_Satellite_Data(s_TLE, &s_data);
}







