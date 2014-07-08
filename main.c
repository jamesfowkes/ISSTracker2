/*
 * main.c
 *
 *  Satellite tracker application
 *
 *  Created on: 02 July 2014
 *      Author: james
 *
 *		Target: ATMEGA328P
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
 * Device Includes
 */

#include "lcd/lcd.h"

/*
 * Generic Library Includes
 */

#include "button.h"
#include "ringbuf.h"
#include "statemachinemanager.h"
#include "statemachine.h"

/*
 * AVR Library Includes
 */

#include "lib_clk.h"
#include "lib_io.h"
#include "lib_tmr8_tick.h"

/*
 * Utility Library Includes
 */
 
#include "util_time.h"
#include "util_geo.h"

/*
 * Application Includes
 */

#include "tlehandler.h"
#include "app_test_harness.h"

/*
 * Private Defines and Datatypes
 */

#define BLINK_TICK_MS 500

enum states
{
	IDLE, MOVING, UPDATING
};
typedef enum states STATES;

enum events
{
	UPDATE_BUTTON_PRESS,
	NEW_POSITION,
	BTN_IDLE,
	MOVE_COMPLETE,
	UDPATE_COMPLETE
};
typedef enum events EVENTS;

/*
 * Function Prototypes
 */
 
static void setupStateMachine(void);
static void setupTimer(void);
//static void onRTCOverflow(void);

static void startUpdate(SM_STATEID old, SM_STATEID new, SM_EVENT e);
static void startMoving(SM_STATEID old, SM_STATEID new, SM_EVENT e);
static void updateTarget(SM_STATEID old, SM_STATEID new, SM_EVENT e);

/*
 * Private Variables
 */

static TMR8_TICK_CONFIG heartbeatTick;

//static TM s_time;

static int8_t sm_index = 0;

static const SM_STATE s_stateIdle = {IDLE, NULL, NULL};
static const SM_STATE s_stateMoving = {MOVING, NULL, NULL};
static const SM_STATE s_stateUpdating = {UPDATING, NULL, NULL};

static SM_ENTRY sm[] = {
	{ &s_stateIdle, 	UPDATE_BUTTON_PRESS,	startUpdate,	&s_stateUpdating },
	{ &s_stateIdle, 	NEW_POSITION, 			startMoving,	&s_stateMoving },
	
	{ &s_stateMoving,	NEW_POSITION, 			updateTarget, 	&s_stateUpdating },
	{ &s_stateMoving,	MOVE_COMPLETE, 			NULL, 			&s_stateIdle },
	
	{ &s_stateUpdating, UDPATE_COMPLETE,		NULL,			&s_stateIdle },
};

int main(void)
{

	/* Disable watchdog: not required for this application */
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	setupStateMachine();
	setupTimer();
	
	TLE_Handler_Init();
	
	DO_TEST_HARNESS_SETUP();
	
	/* All processing interrupt based from here*/
	
	sei();

	while (true)
	{
	
		DO_TEST_HARNESS_RUNNING();
		
		if (TMR8_Tick_TestAndClear(&heartbeatTick))
		{
			// TODO: Blink LED
			DO_TEST_HARNESS_TICK();
		}
		
		//TLE_Handler_Update(&s_time);
	}

	return 0;
}


static void setupTimer(void)
{
	CLK_Init(0);
	TMR8_Tick_Init(1, 0);
	
	heartbeatTick.reload = BLINK_TICK_MS;
	heartbeatTick.active = true;
	TMR8_Tick_AddTimerConfig(&heartbeatTick);
	
	//TODO: Setup 16-bit timer as RTC
}

static void setupStateMachine(void)
{
	SMM_Config(1, 5);
	sm_index = SM_Init(&s_stateIdle, (SM_EVENT)UDPATE_COMPLETE, (SM_STATEID)UPDATING, sm);
	SM_SetActive(sm_index, true);
}

/*static void onRTCOverflow(void)
{
	time_increment_seconds(&s_time);
}*/

static void startUpdate(SM_STATEID old, SM_STATEID new, SM_EVENT e)
{
	(void)old; (void)new; (void)e;
}

static void startMoving(SM_STATEID old, SM_STATEID new, SM_EVENT e)
{
	(void)old; (void)new; (void)e;
}

static void updateTarget(SM_STATEID old, SM_STATEID new, SM_EVENT e)
{
	(void)old; (void)new; (void)e;
}





