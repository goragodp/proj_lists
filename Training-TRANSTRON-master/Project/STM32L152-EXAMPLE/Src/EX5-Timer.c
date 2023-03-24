#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void TIM2_Config(void);

/* TIM handle declaration */
TIM_HandleTypeDef    hTIM2;
/* Prescaler declaration */
uint32_t uwPrescalerValue = 0;
uint32_t counter_value = 0;

void GPIO_Config(void)
{		
	GPIO_InitTypeDef GPIO_InitStructure;
	__HAL_RCC_GPIOB_CLK_ENABLE();

	GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStructure.Pin = GPIO_PIN_6;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStructure);
	
}
int main()
{
	HAL_Init();
	SystemClock_Config();
	GPIO_Config();
	TIM2_Config();
	
	if(HAL_TIM_Base_Start(&hTIM2) != HAL_OK){
		Error_Handler();
	}

	
	while(1)
	{
		if(hTIM2.Instance->CNT == hTIM2.Init.Period)
		{
			HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_6);
		}
	}
}

void TIM2_Config(void)
{		
	__TIM2_CLK_ENABLE();
	//Prescaled system clock to gain counting as 100000 Hz
	uwPrescalerValue = (uint32_t)(SystemCoreClock / 10000) - 1;
	hTIM2.Instance = TIM2; //Config TIM peripheral to utilize Timer 2
	hTIM2.Init.Period = 500 - 1;
	hTIM2.Init.Prescaler = uwPrescalerValue;
	hTIM2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
	hTIM2.Init.CounterMode = TIM_COUNTERMODE_UP;
	
	if(HAL_TIM_Base_Init(&hTIM2) != HAL_OK)
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
