#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void DAC_Config(void);

DAC_HandleTypeDef hDAC;
uint16_t ADC_Value = 0;
uint16_t NbrMeas = 0;
int main()
{
	HAL_Init();
	SystemClock_Config();
	
	DAC_Config();
	
	  /*##-4- Enable DAC Channel1 ################################################*/
  if (HAL_DAC_Start(&hDAC, DAC_CHANNEL_1) != HAL_OK)
  {
    /* Start Error */
    Error_Handler();
  }
  while (1)
  {


	}
}

void GPIO_Config(void)
{		
	GPIO_InitTypeDef GPIO_InitStructure;
	__HAL_RCC_GPIOA_CLK_ENABLE();
	
	GPIO_InitStructure.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStructure.Pin = GPIO_PIN_4;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStructure);

}

void DAC_Config(void)
{
	DAC_ChannelConfTypeDef DAC_ChannelConfStructInit;
	
	GPIO_Config();
	__HAL_RCC_DAC_CLK_ENABLE();
	
	hDAC.Instance = DAC;
	
	if (HAL_DAC_Init(&hDAC) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }
	
	DAC_ChannelConfStructInit.DAC_Trigger = DAC_TRIGGER_NONE;
	DAC_ChannelConfStructInit.DAC_OutputBuffer = DAC_OUTPUTBUFFER_DISABLE;
	
	if (HAL_DAC_ConfigChannel(&hDAC, &DAC_ChannelConfStructInit, DAC_CHANNEL_1) != HAL_OK)
  {
    /* Channel configuration Error */
    Error_Handler();
  }
	
	  /*##-3- Set DAC Channel1 DHR register ######################################*/
  if (HAL_DAC_SetValue(&hDAC, DAC_CHANNEL_1, DAC_ALIGN_8B_R, 0x7F) != HAL_OK)
  {
    /* Setting value Error */
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
