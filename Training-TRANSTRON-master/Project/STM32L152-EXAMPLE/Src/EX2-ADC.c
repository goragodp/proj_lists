#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void ADC_Config(void);

ADC_HandleTypeDef hADC;
uint16_t ADC_Value = 0;
uint16_t NbrMeas = 0;
int main()
{
	HAL_Init();
	SystemClock_Config();
	
	ADC_Config();
	
  HAL_ADC_Start(&hADC);
  while (1)
  {
    if (HAL_ADC_PollForConversion(&hADC, 1000000) == HAL_OK)
    {
       ADC_Value = HAL_ADC_GetValue(&hADC);
       NbrMeas++;
    }
	}
}

void GPIO_Config(void)
{		
	GPIO_InitTypeDef GPIO_InitStructure;
	__HAL_RCC_GPIOA_CLK_ENABLE();
	
	GPIO_InitStructure.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStructure.Pin = GPIO_PIN_1;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(GPIOC, &GPIO_InitStructure);
}

void ADC_Config(void)
{
	ADC_ChannelConfTypeDef ADC_ChannelInitTypeDef;
	
	__ADC1_CLK_ENABLE();
	GPIO_Config();
	
	hADC.Instance = ADC1;
	
	hADC.Init.ClockPrescaler = ADC_CLOCK_ASYNC_DIV1;
	hADC.Init.Resolution = ADC_RESOLUTION_12B;
	hADC.Init.DataAlign = ADC_DATAALIGN_RIGHT;
	hADC.Init.ScanConvMode = DISABLE;
	hADC.Init.ContinuousConvMode = ENABLE;
	hADC.Init.DiscontinuousConvMode = DISABLE;
	hADC.Init.NbrOfConversion = 0;
	hADC.Init.ExternalTrigConv = ADC_SOFTWARE_START;
	hADC.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
	hADC.Init.NbrOfConversion = 1;
	hADC.Init.DMAContinuousRequests = ENABLE;
	hADC.Init.EOCSelection = DISABLE;
	
	HAL_ADC_Init(&hADC);
	
	ADC_ChannelInitTypeDef.Channel = ADC_CHANNEL_11;
	ADC_ChannelInitTypeDef.Rank = 1;
	ADC_ChannelInitTypeDef.SamplingTime = ADC_SAMPLETIME_16CYCLES;
	
	if(HAL_ADC_ConfigChannel(&hADC, &ADC_ChannelInitTypeDef) != HAL_OK)
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
