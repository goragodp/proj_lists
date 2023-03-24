#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void SPI_Config(void);
void DMA_Config(void);

SPI_HandleTypeDef hSPIx;
DMA_HandleTypeDef hDMAx_SPI_RX;
DMA_HandleTypeDef hDMAx_SPI_TX;

/* Buffer used for transmission */
uint8_t aTxBuffer[] = "This data from master";
uint8_t aRxBuffer[sizeof(aTxBuffer)];

int main()
{
	HAL_Init();
	SystemClock_Config();
	
	GPIO_Config();
	SPI_Config();
	DMA_Config();
	
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, GPIO_PIN_RESET);
	while(HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) != SET);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, GPIO_PIN_RESET);
	
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, GPIO_PIN_RESET);
  HAL_SPI_TransmitReceive_DMA(&hSPIx, (uint8_t *)aTxBuffer, (uint8_t*)aRxBuffer, sizeof(aTxBuffer) + 1);
	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, GPIO_PIN_SET);

   for (;;)
   {

   }

	
}

void GPIO_Config(void)
{
	 GPIO_InitTypeDef GPIO_InitStruct;
	
	 __HAL_RCC_GPIOB_CLK_ENABLE();
	 __HAL_RCC_GPIOA_CLK_ENABLE();
	
   /* SPI SCK GPIO pin configuration  */
    GPIO_InitStruct.Pin       = GPIO_PIN_13;
    GPIO_InitStruct.Mode      = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull      = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* SPI MISO GPIO pin configuration  */
    GPIO_InitStruct.Pin = GPIO_PIN_14;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* SPI MOSI GPIO pin configuration  */
    GPIO_InitStruct.Pin = GPIO_PIN_15;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
		
		/* SPI CS GPIO Pin configuration */
		GPIO_InitStruct.Pin = GPIO_PIN_12;
		GPIO_InitStruct.Mode   = GPIO_MODE_OUTPUT_PP;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
		
		/* USER Pin configuration */
		GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
		GPIO_InitStruct.Pin = GPIO_PIN_0;
		GPIO_InitStruct.Pull = GPIO_NOPULL;
		GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
		HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
		
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
		GPIO_InitStruct.Pin = GPIO_PIN_6 | GPIO_PIN_7;
		GPIO_InitStruct.Pull = GPIO_NOPULL;
		GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
		HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}

void SPI_Config(void)
{
	__HAL_RCC_SPI2_CLK_ENABLE();
  hSPIx.Instance               = SPI2;

  hSPIx.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_256;
  hSPIx.Init.Direction         = SPI_DIRECTION_2LINES;
  hSPIx.Init.CLKPhase          = SPI_PHASE_1EDGE;
  hSPIx.Init.CLKPolarity       = SPI_POLARITY_LOW;
  hSPIx.Init.CRCCalculation    = SPI_CRCCALCULATION_DISABLE;
  hSPIx.Init.CRCPolynomial     = 7;
  hSPIx.Init.DataSize          = SPI_DATASIZE_8BIT;
  hSPIx.Init.FirstBit          = SPI_FIRSTBIT_MSB;
  hSPIx.Init.NSS               = SPI_NSS_SOFT;
  hSPIx.Init.TIMode            = SPI_TIMODE_DISABLE;
	hSPIx.Init.Mode 						 = SPI_MODE_MASTER;
	
	 if(HAL_SPI_Init(&hSPIx) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }
	
}

void DMA_Config(void)
{
		__HAL_RCC_DMA1_CLK_ENABLE();
    hDMAx_SPI_RX.Instance = DMA1_Channel4;
    hDMAx_SPI_RX.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hDMAx_SPI_RX.Init.PeriphInc = DMA_PINC_DISABLE;
    hDMAx_SPI_RX.Init.MemInc = DMA_MINC_ENABLE;
    hDMAx_SPI_RX.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hDMAx_SPI_RX.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hDMAx_SPI_RX.Init.Mode = DMA_CIRCULAR;
    hDMAx_SPI_RX.Init.Priority = DMA_PRIORITY_LOW;
    if (HAL_DMA_Init(&hDMAx_SPI_RX) != HAL_OK)
    {
      Error_Handler();
    }

    __HAL_LINKDMA(&hSPIx,hdmarx,hDMAx_SPI_RX);
		HAL_NVIC_SetPriority(DMA1_Channel4_IRQn, 0, 0);
		HAL_NVIC_EnableIRQ(DMA1_Channel4_IRQn);
		
		hDMAx_SPI_TX.Instance = DMA1_Channel5;
		hDMAx_SPI_TX.Init.Direction = DMA_MEMORY_TO_PERIPH;
		hDMAx_SPI_TX.Init.PeriphInc = DMA_PINC_DISABLE;
		hDMAx_SPI_TX.Init.MemInc = DMA_MINC_ENABLE;
		hDMAx_SPI_TX.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
		hDMAx_SPI_TX.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
		hDMAx_SPI_TX.Init.Mode = DMA_CIRCULAR;
		hDMAx_SPI_TX.Init.Priority = DMA_PRIORITY_VERY_HIGH;
		HAL_DMA_Init(&hDMAx_SPI_TX);
 
		__HAL_LINKDMA(&hSPIx,hdmatx,hDMAx_SPI_TX);
		HAL_NVIC_SetPriority(DMA1_Channel5_IRQn, 0, 0);
		HAL_NVIC_EnableIRQ(DMA1_Channel5_IRQn);
}

void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if (hspi->Instance == hSPIx.Instance)
    {
        __NOP();
    }
}

void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if (hspi->Instance == hSPIx.Instance)
    {
        __NOP();
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
