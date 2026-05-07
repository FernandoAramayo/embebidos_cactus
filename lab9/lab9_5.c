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
#include "utils/uartstdio.c"


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
void setup_uart();
void setup_pwm();


// Variables
uint32_t g_ui32SysClock;
//uint32_t potValue[1];


// Definición de velocidades (ajusta según el periodo de 6000 que definiste)
#define VELOCIDAD_ALTA 5000
#define VELOCIDAD_CERO 1

int main(void)
{
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    setup_gpio();
    setup_uart();
    setup_pwm();

    UARTprintf("Sistema de seguimiento listo...\n");

    while(1)
    {
        // Verificar si hay datos disponibles en el UART
        if(UARTCharsAvail(UART0_BASE))
        {
            // Leer el comando enviado por la Raspy 
            char command = UARTCharGet(UART0_BASE);
            
            switch(command)
            {
                case 'F': // Adelante: Ambos motores encendidos
                    GPIOPinWrite(GPIO_PORTE_BASE, 0x05, 0x05); 
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, VELOCIDAD_ALTA);
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, VELOCIDAD_ALTA);
                    break;
        
                case 'L': // Izquierda: Motor Izquierdo (OUT 6) OFF, Motor Derecho (OUT 7) ON
                    GPIOPinWrite(GPIO_PORTE_BASE, 0x05, 0x04); 
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, VELOCIDAD_CERO);
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, VELOCIDAD_ALTA);
                    break;
        
                case 'R': // Derecha: Motor Izquierdo (OUT 6) ON, Motor Derecho (OUT 7) OFF
                    GPIOPinWrite(GPIO_PORTE_BASE, 0x05, 0x01); 
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, VELOCIDAD_ALTA);
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, VELOCIDAD_CERO);
                    break;
        
                case 'S': // Parar: Ambos motores apagados
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, VELOCIDAD_CERO);
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, VELOCIDAD_CERO);
                    break;
}
        }
    }
}

void setup_gpio() {
    // // Enable peripherals
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOE))
         {
         }

    // SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    // while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    //     {
    //     }

    // // Declare otuputs
    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, 0x05);

    // // Declare inputs
    // GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    // GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // [MARKER_GPIO_CONFIG]
}

void setup_uart() {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_UART0)) {}

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA)) {}
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, 0X03);

    UARTStdioConfig(0,9600,120000000);

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
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK)) {}

    // Configurar PK4 y PK5 para PWM (Generador 3 del Módulo 0)
    GPIOPinConfigure(GPIO_PK4_M0PWM6);
    GPIOPinConfigure(GPIO_PK5_M0PWM7);
    GPIOPinTypePWM(GPIO_PORTK_BASE, GPIO_PIN_4 | GPIO_PIN_5);

    PWMGenConfigure(PWM0_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_3, 6000);

    // Inicializar ambos motores en 0 (VELOCIDAD_CERO)
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6, 1);
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1);

    PWMGenEnable(PWM0_BASE, PWM_GEN_3);

    // Habilitar ambas salidas
    PWMOutputState(PWM0_BASE, (PWM_OUT_6_BIT | PWM_OUT_7_BIT), true);
}
