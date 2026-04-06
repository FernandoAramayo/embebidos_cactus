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
void setup_timer();
void setup_uart();
void setup_adc();
void setup_pwm();

// Handler functions declarations
void timer0A_handler(void);

// Variables
uint32_t g_ui32SysClock;
//uint32_t potValue[1];


int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    //setup_gpio();

    //setup_timer();

    //setup_uart();

    //setup_adc();

    //setup_pwm();

    // Loop
    while(1)
    {
    }
}

void setup_gpio() {
    // // Enable peripherals
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    //     {
    //     }

    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    //     {
    //     }

    // // Declare otuputs
    // GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03);

    // // Declare inputs
    // GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    // GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // [MARKER_GPIO_CONFIG]
}

void setup_timer() {
    // Enable global processor interrupts
    IntMasterEnable();

    // // Enable the peripheral
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);

    // // Set timer mode
    // TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    // // Set load value
    // TimerLoadSet(TIMER0_BASE, TIMER_A, g_ui32SysClock*2);

    // // Enable timer interrupt
    // IntEnable(INT_TIMER0A);

    // // Enable specific timer interrupt (timer A interrupt)
    // TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // // Start timer
    // TimerEnable(TIMER0_BASE, TIMER_A);

    // [MARKER_TIM_CONFIG]
}

// Interrupt handler
void timer0A_handler(void)
{
    // Clear the timer interrupt
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);

    // Interrupt code

}

void setup_uart() {
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_UART0)) {}

    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA)) {}
    // GPIOPinConfigure(GPIO_PA0_U0RX);
    // GPIOPinConfigure(GPIO_PA1_U0TX);
    // GPIOPinTypeUART(GPIO_PORTA_BASE, 0X03);

    // UARTStdioConfig(0,9600,120000000);

    // [MARKER_UART_CONFIG]
}

void setup_adc() {
    // // Enable ADC (ADC0 or ADC1)
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0)) {}
    // // Enable pin peripheral and pin
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOD)) {}
    // GPIOPinTypeADC(GPIO_PORTD_BASE, GPIO_PIN_4);
    // // Configures the trigger source and priority of a sample sequence (3 = 1 sample) (Base, sequence, trigger, priority).
    // ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0);
    // // Configures a step of the sample sequencer (Base, sequence, step, configuration flags)
    // ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_IE | ADC_CTL_END | ADC_CTL_CH7);
    // ADCSequenceEnable(ADC0_BASE, 3);
    // // Clear sample sequence interrupt source
    // ADCIntClear(ADC0_BASE, 3);

    // [MARKER_ADC_CONFIG]
}

void setup_pwm() {
    // // Enable M0 PWM module
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    // // Enable selected output pin peripheral 
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}
    // // Configure the pin to PWM function (PF1 is output 1 of module M0)
    // GPIOPinConfigure(GPIO_PF1_M0PWM1);
    // GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1);
    // // Configure count mode (count-down)
    // PWMGenConfigure(PWM0_BASE, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    // // Specify 100% value (clock_freq/pwm_freq)
    // PWMGenPeriodSet(PWM0_BASE, PWM_GEN_0, 6000);
    // // Set initial duty_cylce
    // PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 1);
    // // Start the timer
    // PWMGenEnable(PWM0_BASE, PWM_GEN_0);
    // // Enable outputs
    // PWMOutputState(PWM0_BASE, (PWM_OUT_1_BIT), true);

    // [MARKER_PWM_CONFIG]
}