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
#include <string.h>


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

// Function declarations
void check_buttons();
void check_buzzer();
void delay(uint32_t ms);
uint32_t medir_distancia_cm(void);
void check_distance();

// Variables
uint32_t g_ui32SysClock;
char data[16];

bool g_bButton1Pressed = false;
bool g_bButton2Pressed = false;

bool buzzer_on = false;

int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    setup_gpio();

    //setup_timer();

    setup_uart();

    //setup_adc();

    //setup_pwm();

    // Loop
    while(1)
    {
        //UARTprintf("motor1 \n");
        check_buttons();
        //delay(100);
        check_buzzer();
        check_distance();
        delay(10);

    }
}

void setup_gpio() {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
        {
        }


    // Declare inputs
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK))
        {
        }

    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, GPIO_PIN_0);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOB)) 
    {
    }

    //ECHO
    GPIOPinTypeGPIOInput(GPIO_PORTB_BASE, 0x10);
    //TRIG
    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE, 0x20);


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

void setup_uart()
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_UART0)){}
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA)){}

    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    GPIOPinTypeUART(GPIO_PORTA_BASE, 0x03);

    UARTStdioConfig(0, 9600, g_ui32SysClock);
}

void setup_adc() {


    // [MARKER_ADC_CONFIG]
}

void setup_pwm() {
    // Configuración PWM M0, Salida 5 (Port G, Pin 1)
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOG)) {}
    
    GPIOPinConfigure(GPIO_PG1_M0PWM5);
    GPIOPinTypePWM(GPIO_PORTG_BASE, GPIO_PIN_1);
    PWMGenConfigure(PWM0_BASE, PWM_GEN_2, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    
    uint32_t ui32PeriodM0_5 = g_ui32SysClock / 20000;
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_2, ui32PeriodM0_5);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_5, (ui32PeriodM0_5 * 55) / 100);
    
    PWMGenEnable(PWM0_BASE, PWM_GEN_2);
    PWMOutputState(PWM0_BASE, PWM_OUT_5_BIT, true);

    // [MARKER_PWM_CONFIG]
}

void check_buttons() {
    // Leer el estado de los botones 
    // Botón 1 (PJ0)
    if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
    {
        UARTprintf("motor1\n");
        delay(10);
    }

    // Botón 2 (PJ1)
    if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0)
    {
        UARTprintf("motor2\n");
        delay(10);

    }
}

void check_buzzer() {
    if(UARTCharsAvail(UART0_BASE)) {
        UARTgets(data,16);
        if(*data == 'b'){
           GPIOPinWrite(GPIO_PORTK_BASE, 0x01, 0x01);
           delay(2000);
           GPIOPinWrite(GPIO_PORTK_BASE, 0x01, 0);

        }         
    }
}

uint32_t medir_distancia_cm(void)
{
    uint32_t tiempo = 0;
    int timeout;

    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, 0x00);
    delay(1);

    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, 0x20);
    delay(1);
    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, 0x00);

    timeout = 1000;
    while(GPIOPinRead(GPIO_PORTB_BASE, GPIO_PIN_4) == 0 && timeout > 0)
    {
        timeout--;
        delay(1);
    }

    if(timeout == 0)
        return 999;

    timeout = 1000;
    while(GPIOPinRead(GPIO_PORTB_BASE, GPIO_PIN_4) != 0 && timeout > 0)
    {
        tiempo++;
        timeout--;
        delay(1);
    }

    if(timeout == 0)
        return 999;

    return (34300 * tiempo) / 2000;
}

void delay(uint32_t ms)
{
    SysCtlDelay((g_ui32SysClock / 1000) * ms / 3);
}

void check_distance() 
{
    uint32_t distancia = medir_distancia_cm();
    if(distancia <= 3) {
        UARTprintf("stop\n");
    }
}
