include $(PROJECTS_PATH)/Libs/standard.mk

NAME = isstracker2_test
CC = gcc 
EXTRA_FLAGS = -DF_CPU=16000000 -DMEMORY_POOL_BYTES=512
MMCU = iom128

EXTRA_INCLUDE_DIRS = \
	-I$(LIBS_DIR)/AVR \
	-I$(LIBS_DIR)/Common \
	-I$(LIBS_DIR)/Devices \
	-I$(LIBS_DIR)/Generics \
	-I$(LIBS_DIR)/Utility

EXTRA_CFILES = \
	app_test_harness.c \
	main.c \
	tlehandler.c \
	$(LIBS_DIR)/AVR/lib_clk.c \
	$(LIBS_DIR)/AVR/lib_fuses.c \
	$(LIBS_DIR)/AVR/lib_io.c \
	$(LIBS_DIR)/AVR/lib_tmr8.c \
	$(LIBS_DIR)/AVR/lib_tmr8_tick.c \
	$(LIBS_DIR)/Devices/lcd/lcd.c \
	$(LIBS_DIR)/Generics/memorypool.c \
	$(LIBS_DIR)/Generics/ringbuf.c \
	$(LIBS_DIR)/Generics/statemachinemanager.c \
	$(LIBS_DIR)/Generics/statemachine.c \
	$(LIBS_DIR)/Utility/util_geo.c \
	$(SGP_DIR)/sgp_conv.c \
	$(SGP_DIR)/sgp_deep.c \
	$(SGP_DIR)/sgp_math.c \
	$(SGP_DIR)/sgp_time.c \
	$(SGP_DIR)/sgp4sdp4.c

include $(LIBS_DIR)/AVR/Harness/make_test_harness.mk
