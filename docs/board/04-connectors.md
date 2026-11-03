# 4. Connectors and pinout

![The connections of the control board](../assets/img_parol3.webp){ width="750" }

## Connectors

| Connection | Connector |
|---|---|
| 24 V power | XT30 male |
| Cooling fan | 3-pin, 2.54 mm pitch, 5 V |
| Power button | JST PH 4-pin (B4B-PH-SM4-TB) |
| USB | USB type B |
| Programming | 2×5-pin, 2.54 mm pitch (SWD) |
| Motors | 6 × 4-pin terminal blocks, one per driver |
| Limit switches, inputs, outputs, E-stop, CAN, 24 V out, GND, HV_SEL, GND_SEL | Pluggable terminal blocks along the edges |

## Which parts of the board belong to which joint

Each joint uses three things on the board: the terminals its motor plugs into, the driver module that powers
that motor, and the input its limit switch or sensor is wired to. The board labels them with three different
numberings, and only the motor terminals use the joint's own number:

| Joint | Motor terminals | Driver module socket | Limit switch or sensor input |
|---|---|---|---|
| 1 | `J1_A+` `J1_A-` `J1_B+` `J1_B-` | MOTOR1 | **Limit 6** |
| 2 | `J2_…` | **MOTOR6** | Limit 2 |
| 3 | `J3_…` | **MOTOR5** | Limit 3 |
| 4 | `J4_…` | MOTOR4 | Limit 4 |
| 5 | `J5_…` | **MOTOR2** | Limit 5 |
| 6 | `J6_…` | **MOTOR3** | **Limit 1** |

- **Motors:** connect each joint's motor to the terminals marked with its joint number. The board routes them to
  the right driver; nothing to remap.
- **Limit switches and sensors:** joints 2 to 5 go to the input with their own number, but joints 1 and 6 are
  swapped: joint 1's sensor goes to **Limit 6**, joint 6's sensor to **Limit 1**.
- **Driver modules:** the sockets MOTOR1 to MOTOR6 are not in joint order. All six modules are the same, so this
  only matters when one is faulty: the joint that misbehaves tells you which socket to look at.

The firmware sets this up in `motor_init.cpp` (each joint's step, select and limit pins). When in doubt, let the
test firmware check it: `#LIMIT` prints `Joint N is pressed` for each switch you press
([The test firmware](09-test-firmware.md)).

## Pin definitions

The microcontroller pins as the firmware defines them (`iodefs.h`), for anyone who writes firmware or probes the
board:

```c
#define PUL1 PC6     // step, joint 1          #define DIR1 PB15    // direction, joint 1
#define PUL2 PA10    // step, joint 5          #define DIR2 PA1     // direction, joint 5
#define PUL3 PC0     // step, joint 6          #define DIR3 PC1     // direction, joint 6
#define PUL4 PC3     // step, joint 4          #define DIR4 PA0     // direction, joint 4
#define PUL5 PC9     // step, joint 3          #define DIR5 PA8     // direction, joint 3
#define PUL6 PC5     // step, joint 2          #define DIR6 PB1     // direction, joint 2

#define SELECT1 PC7  // SPI chip select of driver 1 (joint 1)
#define SELECT2 PA9  // driver 2 (joint 5)
#define SELECT3 PC15 // driver 3 (joint 6)
#define SELECT4 PC2  // driver 4 (joint 4)
#define SELECT5 PC8  // driver 5 (joint 3)
#define SELECT6 PC4  // driver 6 (joint 2)
#define GLOBAL_ENABLE PA3   // ENABLE of all drivers

#define LIMIT1 PC12  // LIMIT 1 terminal (joint 6)   #define LIMIT4 PD2   // LIMIT 4 (joint 4)
#define LIMIT2 PB3   // LIMIT 2 (joint 2)            #define LIMIT5 PB4   // LIMIT 5 (joint 5)
#define LIMIT3 PA15  // LIMIT 3 (joint 3)            #define LIMIT6 PC11  // LIMIT 6 (joint 1)

#define MISO PA6, MOSI PA7, SCK PA5   // SPI to the six drivers and the flash
#define FLASH_SELECT PA4              // chip select of the flash memory

#define LED1 PB2, LED2 PB10           // the two LEDs
#define SUPPLY_ON_OFF PC10            // switches the 24 V power stage
#define SUPPLY_BUTTON_STATE PC14      // reads the power button
#define INPUT1 PB6, INPUT2 PB5        // IN1, IN2 terminals
#define OUTPUT1 PC13, OUTPUT2 PB7     // OUT1, OUT2 terminals
#define ESTOP PB14                    // E-stop terminals
#define VBUS PB0                      // supply voltage sense
#define USB_D_PLUS PA12, USB_D_MINUS PA11
#define CAN1TX PB9, CAN1RX PB8        // CAN 1 (the gripper bus)
#define CAN2TX PB13, CAN2RX PB12      // CAN 2 (transceiver not populated)
```

## Wiring the robot

![Wiring diagram of the robot to the control board](../assets/parol6v2_connection.webp){ width="750" }

Limit switches to 24 V and their LIMIT terminal; inductive sensors to 24 V, GND and the LIMIT terminal (brown,
blue, black). The gripper's M8 socket to 24 V, GND, CAN H and CAN L. The finished wiring in PAROL6's base:

![The wired board](../assets/WIRING V2.webp){ width="650" }

![The connectors at the base](../assets/CONNECT.webp){ width="650" }
