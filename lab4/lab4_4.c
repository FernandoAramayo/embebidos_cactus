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
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/timer.h"


// Variables
uint32_t g_ui32SysClock;
int counter = 0;
bool three_seconds_interval = false;


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

// setup functions declarations
void setup_gpio();
void setup_timer();

// handler functions declarations
void Timer0IntHandler(void);

int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    setup_gpio();

    setup_timer();

    // Loop
    while(1)
    {
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
            three_seconds_interval = !three_seconds_interval;
            SysCtlDelay((g_ui32SysClock / 1000) * 200 / 3);
            while(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {}
        }
    }
}

void setup_gpio() {
    // Enable peripherals
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

    // Declare otuputs
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4);

    // Declare inputs
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
}

void setup_timer() {
    // Enable the peripheral
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // Enable global processor interrupts
    IntMasterEnable();

    // Set timer mode
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    // Set load value
    TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*1.5);

    // Enable timer interrupt
    IntEnable(INT_TIMER0A);

    // Enable specific timer interrupt (timer A interrupt)
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Start timer
    TimerEnable(TIMER0_BASE, TIMER_A);
}

// Interrupt handler
void Timer0IntHandler(void)
{
    // Clear the timer interrupt.
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    if (three_seconds_interval) TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*3);
    else TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*1.5);

    if (counter < 15) counter++;
    else if (counter == 15) {
        counter = 0;
        GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_4, 0);
        GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0 | GPIO_PIN_1, 0);
    }

    if (counter & 0x01) GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    else GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0);

    if (counter & 0x02) GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    else GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0);

    if (counter & 0x04) GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    else GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0);

    if (counter & 0x08) GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    else GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0);
}
