#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

//*****************************************************************************
//
//! \addtogroup example_list
//! <h1>Blinky (blinky)</h1>
//!
//! A very simple example that blinks the on-board LED using direct register
//! access.
//
//*****************************************************************************

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

// Function declarations
void delay(uint32_t ms);

// Variables
uint32_t g_ui32SysClock;
int state = 1;

int
main(void)
{
    //volatile uint32_t ui32Loop;

    // Enable system clock
    g_ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                         SYSCTL_OSC_MAIN |
                                         SYSCTL_USE_PLL |
                                         SYSCTL_CFG_VCO_480), 120000000);
                                         
    // Enable the GPIO ports
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    {
    }

    // Enable the GPIO pins 
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4);

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU); 

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU); 

    // Loop forever.
    while(1)
    {
        // Check buttons
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0 && state < 4) {
            state++;
            delay(200);
            while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {}
        }
        else if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0 && state > 1) {
            state--;
            delay(200);
            while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {}
        }

        switch (state) {
            case 1:
                {
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_1);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
                    break;
                }
                case 2:
                {
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_0 | GPIO_PIN_1);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
                    break;
                }
                case 3:
                {
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_0 | GPIO_PIN_1);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, GPIO_PIN_4);
                    break;
                }
                case 4:
                {
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, GPIO_PIN_0 | GPIO_PIN_1);
                    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, GPIO_PIN_0 | GPIO_PIN_4);
                    break;
                }
                default:
                    break;
        }
    }
}


// Delay in miliseconds
void delay(uint32_t ms)
{
    SysCtlDelay((g_ui32SysClock / 1000) * ms / 3);
}
