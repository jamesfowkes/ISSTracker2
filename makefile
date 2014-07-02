NAME=isstracker2

MCU_TARGET=atmega128

CC=avr-gcc 
LD=avr-ld
SIZE=avr-size

LIBS_DIR = $(PROJECTS_PATH)/Libs
DEL = python $(LIBS_DIR)/del.py

SGP_DIR = $(LIBS_DIR)/SGP

SGP_MODEL = SGP4

SGP_FILES = \
	$(SGP_DIR)/sgp_conv.c \
	$(SGP_DIR)/sgp_deep.c \
	$(SGP_DIR)/sgp_math.c \
	$(SGP_DIR)/sgp_time.c \
	$(SGP_DIR)/sgp4sdp4.c

OPT_LEVEL=3

CCFLAGS = \
	-mmcu=$(MCU_TARGET) \
	-g \
	-std=c99 \
	-Wall \
	-Wextra \
	-DF_CPU=16000000 \
	-DMEMORY_POOL_BYTES=512 \
	-DSGP_MODEL_$(SGP_MODEL) \
	-ffunction-sections \
	-fdata-sections \
	-O$(OPT_LEVEL) \
	-DUNIX_TIME_TYPE=uint32_t

LDFLAGS = \
	--gc-sections --relax

LD_SUFFIX = -lm -lc

AVR_FILES = \
	main.c \
	tlehandler.c \
	$(LIBS_DIR)/AVR/lib_clk.c \
	$(LIBS_DIR)/AVR/lib_fuses.c \
	$(LIBS_DIR)/AVR/lib_io.c \
	$(LIBS_DIR)/AVR/lib_tmr8.c \
	$(LIBS_DIR)/AVR/lib_tmr8_tick.c \
	$(LIBS_DIR)/Devices/lcd/lcd.c \
	$(LIBS_DIR)/Generics/memorypool.c
	
ALL_DEPENDENCY_FILES = $(AVR_FILES) $(SGP_FILES) 
ALL_DEPENDENCIES = $(ALL_DEPENDENCY_FILES:.c=.o)

INCLUDES = \
	-I$(SGP_DIR) \
	-I$(LIBS_DIR)/AVR \
	-I$(LIBS_DIR)/Devices \
	-I$(LIBS_DIR)/Generics \
	-I$(LIBS_DIR)/Utility
	
# all
all : $(NAME).elf

# SGPExample.elf
$(NAME).elf : $(ALL_DEPENDENCIES)
	$(CC) $(CCFLAGS) $(LDFLAGS) -o $@ $^ $(LD_SUFFIX)

%.o:%.c
	$(CC) $(INCLUDES) $(CCFLAGS) -c $< -o $@

size:
	$(SIZE) -C $(NAME).elf --mcu=$(MCU_TARGET)
clean :
	$(DEL) $(ALL_DEPENDENCIES)
