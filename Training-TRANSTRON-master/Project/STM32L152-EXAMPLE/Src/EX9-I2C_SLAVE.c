#include "stm32l1xx_hal.h"

#define I2C_ADDRESS 0x30F

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void I2C_Config(void);

I2C_HandleTypeDef hI2Cx;

/* Buffer used for transmission */
uint8_t TxBuffer[] = "This data from slave!";
uint8_t RxBuffer[sizeof(TxBuffer)];

int main()
{
	HAL_Init();
	SystemClock_Config();
	
	GPIO_Config();
	I2C_Config();
	
	
	
  /*##-2- Put I2C peripheral in reception process ############################*/ 
  /* Timeout is set to 10S  */
  if(HAL_I2C_Slave_Receive(&hI2Cx, (uint8_t *)RxBuffer, sizeof(RxBuffer), 10000) != HAL_OK)
  {
    /* Transfer error in reception process */
    Error_Handler();
  }
  
  /* Turn LED1 on: Transfer in reception process is correct */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, GPIO_PIN_SET);
  
  /*##-3- Start the transmission process #####################################*/  
  /* While the I2C in reception process, user can transmit data through 
     "aTxBuffer" buffer */
  /* Timeout is set to 10S */
  if(HAL_I2C_Slave_Transmit(&hI2Cx, (uint8_t*)TxBuffer, sizeof(TxBuffer), 10000)!= HAL_OK)
  {
    /* Transfer error in transmission process */
    Error_Handler();    
  }
  
  /* Turn LED2 on: Transfer in transmission process is correct */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, GPIO_PIN_SET);
	
   while(1)
   {

   }

	
}

void GPIO_Config(void)
{
	 GPIO_InitTypeDef GPIO_InitStruct;
	
	 __HAL_RCC_GPIOB_CLK_ENABLE();
	 __HAL_RCC_GPIOA_CLK_ENABLE();
	
		/* SCL Pin configuratiojn */
    GPIO_InitStruct.Pin = GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF4_I2C2;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
	
		/* SDA Pin configuration */
		GPIO_InitStruct.Pin = GPIO_PIN_11;
		HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
		
		/* LED  configuration */
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
		GPIO_InitStruct.Pin = GPIO_PIN_6 | GPIO_PIN_7;
		GPIO_InitStruct.Pull = GPIO_NOPULL;
		GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
		HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}

void I2C_Config(void)
{
	 __HAL_RCC_I2C2_CLK_ENABLE();
	hI2Cx.Instance = I2C2;
	hI2Cx.Mode = HAL_I2C_MODE_SLAVE;
  hI2Cx.Init.ClockSpeed = 400000;
  hI2Cx.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hI2Cx.Init.OwnAddress1 = 0x30F;
  hI2Cx.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hI2Cx.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hI2Cx.Init.OwnAddress2 = 0;
  hI2Cx.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hI2Cx.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hI2Cx) != HAL_OK)
  {
    Error_Handler();
  }
}

/** System Clock Configuration
*/
void SystemClock_Config(void)
{

  RCC_OscInitTypeDef RCC_OscInitStruct;
  RCC_ClkInitTypeDef RCC_ClkInitStruct;

  __HAL_RCC_PWR_CLK_ENABLE();

  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = 16;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL6;
  RCC_OscInitStruct.PLL.PLLDIV = RCC_PLL_DIV3;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }

  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

  /* SysTick_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler */
  /* User can add his own implementation to report the HAL error return state */
  while(1) 
  {
  }
  /* USER CODE END Error_Handler */ 
}
