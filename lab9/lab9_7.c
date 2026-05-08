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
#include "utils/uartstdio.c" // Mantenido tal como lo tenías en tu código original

//*****************************************************************************
// The error routine that is called if the driver library encounters an error.
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

int main(void)
{
    // Configuración del reloj del sistema a 120 MHz
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_240), 120000000);

    // Inicialización de periféricos
    setup_gpio();
    //setup_timer();
    setup_uart();
    //setup_adc();
    setup_pwm();

    // Variable para guardar el estado de los LEDs en el toggle
    uint8_t led_state = 0;

    // Loop principal
    while(1)
    {
        // 1. Revisar si hay datos entrantes en el UART0 desde la Raspberry
        if (UARTCharsAvail(UART0_BASE)) 
        {
            // Leer el carácter sin bloquear el sistema
            char cmd = UARTCharGetNonBlocking(UART0_BASE);

            // 2. Tomar acción dependiendo de la letra recibida
            switch(cmd) 
            {
                case 'M': // 2 o más objetos: Toggle de 2 LEDs (Pines PE0 y PE2)
                    // Leemos el estado actual de los pines 0 y 2 del puerto E
                    led_state = GPIOPinRead(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_2);
                    // Escribimos lo contrario (~) para hacer que parpadeen
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_2, ~led_state);
                    
                    // Retardo para que el ojo humano pueda ver el parpadeo
                    SysCtlDelay(g_ui32SysClock / 30); 
                    break;

                case 'T': // 0 objetos: Girar lentamente
                    // Reducimos el ancho de pulso del PWM (1000 sobre el periodo de 6000)
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1000); 
                    
                    // Nos aseguramos de apagar los LEDs
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_2, 0x00);
                    break;

                case 'L': // 1 objeto: Ir a la Izquierda
                case 'R': // 1 objeto: Ir a la Derecha
                case 'F': // 1 objeto: Ir al Centro / Adelante
                    // Aumentamos el PWM a velocidad normal para seguimiento (50% = 3000)
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 3000); 
                    
                    // Nos aseguramos de apagar los LEDs
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_2, 0x00);
                    break;
                    
                case 'S': // Detener sistema
                    // Ponemos el PWM al mínimo
                    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1); 
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_2, 0x00);
                    break;
            }
        }
    }
}

// ============================================================================
// FUNCIONES DE CONFIGURACIÓN (Tus funciones originales intactas)
// ============================================================================

void setup_gpio() {
    // Enable peripherals
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOE))
         {
         }

    // Declare otuputs (0x05 habilita los pines PE0 y PE2)
    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, 0x05);

    // [MARKER_GPIO_CONFIG]
}

void setup_timer() {
    // Enable global processor interrupts
    IntMasterEnable();

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
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_UART0)) {}

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOA)) {}
    
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, 0X03); // PA0 y PA1

    UARTStdioConfig(0,9600,120000000);

    // [MARKER_UART_CONFIG]
}

void setup_adc() {
    // [MARKER_ADC_CONFIG]
}

void setup_pwm() {
    // Enable M0 PWM module
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    
    // Enable selected output pin peripheral 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK)) {}
    
    // Configure the pin to PWM function (PK5 is output 7 of module M0)
    GPIOPinConfigure(GPIO_PK5_M0PWM7);
    GPIOPinTypePWM(GPIO_PORTK_BASE, GPIO_PIN_5);
    
    // Configure count mode (count-down)
    PWMGenConfigure(PWM0_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    
    // Specify 100% value (clock_freq/pwm_freq)
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_3, 6000);
    
    // Set initial duty_cylce
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7, 1); // Cambiado a PWM_OUT_7 que corresponde al pin PK5
    
    // Start the timer
    PWMGenEnable(PWM0_BASE, PWM_GEN_3);
    
    // Enable outputs
    PWMOutputState(PWM0_BASE, (PWM_OUT_7_BIT), true);

    // [MARKER_PWM_CONFIG]
}