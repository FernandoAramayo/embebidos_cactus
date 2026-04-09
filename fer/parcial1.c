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

// Setup functions declarations
void setup_gpio();
void setup_timer();
void setup_uart();
void setup_adc();
void setup_pwm();

// Function declarations
void check_buttons();
void check_buzzer();
void delay(uint32_t ms);
void delay_us(uint32_t us);
uint32_t medir_distancia_cm(void);
uint32_t parse_int(const char *str); 
void stop();
void turn();

// Variables
uint32_t g_ui32SysClock;
char data[16];
uint32_t ui32PeriodM0_7;
uint32_t ui32PeriodM0_6;
bool flag = false;

int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    setup_pwm();
    setup_gpio();
    setup_uart();

    // Loop
    while(1)
    {
        check_buttons();
        
        check_buzzer();
        //check_distance(); // Keep disabled until UART is verified
        delay(10);
    }
}

uint32_t parse_int(const char *str) {
    uint32_t result = 0;
    while (*str >= '0' && *str <= '9') {
        result = result * 10 + (*str - '0');
        str++;
    }
    return result;
}

void setup_gpio() {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ)) {}

    // Declare inputs
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK)) {}
    GPIOPinTypeGPIOOutput(GPIO_PORTK_BASE, GPIO_PIN_0);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOB)) {}

    //ECHO & TRIG
    GPIOPinTypeGPIOInput(GPIO_PORTB_BASE, 0x10);
    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE, 0x20);

    // Motor
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOE)) {}

    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, 0x0F);
    GPIOPinWrite(GPIO_PORTE_BASE, 0x0F, 0x0A);
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

void setup_pwm() {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK)) {}
    
    //PWM PK5 (Motor 1 / OUT_7)
    GPIOPinConfigure(GPIO_PK5_M0PWM7);
    GPIOPinTypePWM(GPIO_PORTK_BASE, GPIO_PIN_5);
    PWMGenConfigure(PWM0_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    
    ui32PeriodM0_7 = g_ui32SysClock / 20000;
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_3, ui32PeriodM0_7);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1);
    
    PWMGenEnable(PWM0_BASE, PWM_GEN_3);
    PWMOutputState(PWM0_BASE, PWM_OUT_7_BIT, true);

    //PWM PK4 (Motor 2 / OUT_6)
    GPIOPinConfigure(GPIO_PK4_M0PWM6);
    GPIOPinTypePWM(GPIO_PORTK_BASE, GPIO_PIN_4);
    PWMGenConfigure(PWM0_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    
    ui32PeriodM0_6 = g_ui32SysClock / 20000;
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_3, ui32PeriodM0_6);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 1);
    
    PWMGenEnable(PWM0_BASE, PWM_GEN_3);
    PWMOutputState(PWM0_BASE, PWM_OUT_6_BIT, true);
}

void check_buttons() {
    // Botón 1 (PJ0)
    uint32_t distancia = medir_distancia_cm();
    if (distancia <= 3)
    {
        UARTprintf("stop\n");
        stop();
        delay(500);
        turn();
        return;
    }
    else if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0)
        
    {
        UARTprintf("motor1\n");
        delay(10);
            
            //int timeout = 50000;
        while(!UARTCharsAvail(UART0_BASE)) {}
            
            //if(timeout > 0) {
            UARTgets(data,16);
            uint32_t pwm = parse_int(data);
            pwm = 50 + (pwm / 2);
            pwm = (pwm * ui32PeriodM0_7) / 100;         
            PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, pwm);
            //}
        }

    else 
    {
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1);
    }
    
    if(GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0 && distancia>=3)
    {
         UARTprintf("motor2\n");
         delay(10);
            
            //int timeout = 50000;
         while(!UARTCharsAvail(UART0_BASE)) {}
            
            //if(timeout > 0) {
              UARTgets(data,16);
              uint32_t pwm = parse_int(data);
              pwm = 50 + (pwm / 2);
              pwm = (pwm * ui32PeriodM0_6) / 100;
            //uint32_t pwm = parse_int(data);
              //pwm = (pwm * ui32PeriodM0_6) / 50;
              PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, pwm);
            //}
        }
     else 
     {
         PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 1);
     }
    // Botón 2 (PJ1)
    
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
    uint32_t timeout;

    // TRIG limpio
    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, 0);
    delay_us(2);

    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, GPIO_PIN_5);
    delay_us(10);
    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5, 0);

    // Esperar subida ECHO
    timeout = 30000;
    while(GPIOPinRead(GPIO_PORTB_BASE, GPIO_PIN_4) == 0 && timeout--)
    {
        delay_us(1);
    }

    if(timeout == 0)
        return 999;

    // Medir pulso alto
    timeout = 30000;
    while(GPIOPinRead(GPIO_PORTB_BASE, GPIO_PIN_4) == GPIO_PIN_4 && timeout--)
    {
        tiempo++;
        delay_us(1);
    }

    if(timeout == 0)
        return 999;

    return tiempo / 58;
}

void delay(uint32_t ms)
{
    SysCtlDelay((g_ui32SysClock / 1000) * ms / 3);
}
void delay_us(uint32_t us)
{
    SysCtlDelay((g_ui32SysClock / 3000000) * us);
}
void stop(){
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 1);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1);
    delay(100);
}

void turn() {
    // Modificar motor 1
    UARTprintf("turn1\n");
    delay(10);
    GPIOPinWrite(GPIO_PORTE_BASE, 0x0F, 0x09);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 1800);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1800);
    delay(900);

    UARTprintf("turn2\n");
    delay(10);
    GPIOPinWrite(GPIO_PORTE_BASE, 0x0F, 0x0A);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 3000);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 3000);
}