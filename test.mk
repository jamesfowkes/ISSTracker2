include $(PROJECTS_PATH)/Libs/standard.mk

NAME = isstracker2_test
CC = gcc 
EXTRA_FLAGS = -DF_CPU=16000000 -DMEMORY_POOL_BYTES=512 -DUNIX_TIME_TYPE=uint32_t
MMCU = iom128

SGP_DIR = $(LIBS_DIR)/SGP
SGP_MODEL = SGP4

EXTRA_INCLUDE_DIRS = \
	-I$(LIBS_DIR)/AVR \
	-I$(LIBS_DIR)/Common \
	-I$(LIBS_DIR)/Devices \
	-I$(LIBS_DIR)/Generics \
	-I$(LIBS_DIR)/Utility \
	-I$(SGP_DIR)
	
EXTRA_CFILES = \
	app_test_harness.c \
	main.c \
	tlehandler.c \
	$(LIBS_DIR)/AVR/lib_clk.c \
	$(LIBS_DIR)/AVR/lib_fuses.c \
	$(LIBS_DIR)/AVR/lib_io.c \
	$(LIBS_DIR)/AVR/lib_tmr8.c \
	$(LIBS_DIR)/AVR/lib_tmr8_tick.c \
	$(LIBS_DIR)/Generics/memorypool.c \
	$(LIBS_DIR)/Generics/ringbuf.c \
	$(LIBS_DIR)/Generics/statemachinemanager.c \
	$(LIBS_DIR)/Generics/statemachine.c \
	$(LIBS_DIR)/Utility/util_geo.c

OTHER_OBJS = $(SGP_OBJS)
OTHER_TARGETS = SGP

include $(LIBS_DIR)/AVR/Harness/make_test_harness.mk
include $(LIBS_DIR)/SGP/sgp.mk
