#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void TIMx_PWM_Config(void);
void EXTI0_Config(void);

TIM_MasterConfigTypeDef sMasterConfig;
TIM_HandleTypeDef hTIM2; //Instance used on previous examkple
/* TIM handle declaration */ //TIM4CH2
TIM_HandleTypeDef    hTIMx;
/* Timer Output Compare Configuration Structure declaration */
TIM_OC_InitTypeDef sConfig;
uint32_t uhPrescalerValue;
uint8_t duty = 0;

int main()
{
	HAL_Init();
	SystemClock_Config();
	
	GPIO_Config();
	TIMx_PWM_Config();
	HAL_TIM_Base_Start(&hTIMx);
	EXTI0_Config();
//	if(HAL_TIM_PWM_Start(&hTIMx, TIM_CHANNEL_1) != HAL_OK)
//	{
//		Error_Handler();
//	}
	if(HAL_TIM_PWM_Start(&hTIMx, TIM_CHANNEL_2) != HAL_OK)
	{
		Error_Handler();
	}

	while(1)
	{

	}
}
void GPIO_Config(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	__HAL_RCC_GPIOB_CLK_ENABLE();

	GPIO_InitStructure.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStructure.Pin = GPIO_PIN_6 | GPIO_PIN_7;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Alternate = GPIO_AF2_TIM4;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStructure);
	
}

void TIMx_PWM_Config(void)
{		
	__TIM4_CLK_ENABLE();

	uhPrescalerValue = (uint32_t)(SystemCoreClock / 16000000) - 1;
	
	hTIMx.Instance = TIM4; //Config TIM peripheral to utilize Timer 4
	hTIMx.Init.Period = 666 - 1;
	hTIMx.Init.Prescaler = uhPrescalerValue;
	hTIMx.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
	hTIMx.Init.CounterMode = TIM_COUNTERMODE_UP;
	
	if(HAL_TIM_PWM_Init(&hTIMx) != HAL_OK)
	{
		Error_Handler();
	}
	
	/*TIM4 PWM CH2 Config*/
	sConfig.OCMode = TIM_OCMODE_PWM1;
	sConfig.OCPolarity = TIM_OCPOLARITY_HIGH;
	sConfig.OCFastMode = TIM_OCFAST_DISABLE;
	sConfig.OCIdleState  = TIM_OCIDLESTATE_RESET;
	
	sConfig.Pulse = 666/64;
	if(HAL_TIM_PWM_ConfigChannel(&hTIMx, &sConfig, TIM_CHANNEL_1) != HAL_OK)
	{
		Error_Handler();
	}
	
	sConfig.Pulse = 666;
	if(HAL_TIM_PWM_ConfigChannel(&hTIMx, &sConfig, TIM_CHANNEL_2) != HAL_OK)
	{
		Error_Handler();
	}
}


void EXTI0_Config(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	__HAL_RCC_GPIOA_CLK_ENABLE();

	GPIO_InitStructure.Mode = GPIO_MODE_IT_RISING; //Enable GPIO input mode interrupt, capture on rising edge
	GPIO_InitStructure.Pin = GPIO_PIN_0;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStructure);
	 /* Enable and set EXTI lines 0 Interrupt to the lowest priority */
  HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);
  HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	if(GPIO_Pin == GPIO_PIN_0)
	{	
		(duty == 100)?(duty = 0):(duty += 25);
		sConfig.Pulse = 666*duty/100;
		if(HAL_TIM_PWM_ConfigChannel(&hTIMx, &sConfig, TIM_CHANNEL_2) != HAL_OK)
		{
			Error_Handler();
		}
		
		if(HAL_TIM_PWM_Start(&hTIMx, TIM_CHANNEL_2) != HAL_OK)
		{
			Error_Handler();
		}
	}

}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef* ht)
{
	if(ht->Instance == TIM2)
	{
		HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7,GPIO_PIN_RESET);

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
