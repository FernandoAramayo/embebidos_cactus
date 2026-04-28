#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"
#include "driverlib/adc.h"
#include "driverlib/pwm.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"


//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif

// Setup functions declarations
void setup_gpio();

// Function declarations
void delay(uint32_t ms);

// Variables
uint32_t g_ui32SysClock;
int pin = 0;
int leds[3] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2};

int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    setup_gpio();

    // Loop
    while(1)
    {
        GPIOPinWrite(GPIO_PORTE_BASE, 0x07, leds[pin]);
        if(pin < 2) pin++;
        else pin = 0;
        delay(10000);
    }
}

void setup_gpio() {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOE))
        {
        }

    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, 0x07);
}

void delay(uint32_t ms)
{
    SysCtlDelay((g_ui32SysClock / 1000) * ms / 3);
}