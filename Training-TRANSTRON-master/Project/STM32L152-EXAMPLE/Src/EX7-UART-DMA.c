#include "stm32l1xx_hal.h"

void SystemClock_Config(void);
void Error_Handler(void);

void GPIO_Config(void);
void UART_Config(void);
void DMA_Config(void);


uint8_t aTxBuffer[] = " ****UART_TwoBoards_ComIT****";
uint8_t aRxBuffer[sizeof(aTxBuffer)];

__IO ITStatus UartReady = RESET;


UART_HandleTypeDef hUARTx;
DMA_HandleTypeDef hDMA_RX;
int main()
{
	HAL_Init();
	SystemClock_Config();
	
	GPIO_Config();
	UART_Config();
	DMA_Config();
  
	/*Wait for data until buffer is full*/
	if(HAL_UART_Receive_DMA(&hUARTx, (uint8_t *)aRxBuffer, sizeof(aRxBuffer)) != HAL_OK)
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
	GPIO_InitStructure.Pin = GPIO_PIN_10 | GPIO_PIN_11;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	GPIO_InitStructure.Pull = GPIO_PULLUP;
	GPIO_InitStructure.Alternate = GPIO_AF7_USART3;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStructure);
	
}

void UART_Config(void)
{
	__HAL_RCC_USART3_CLK_ENABLE();
	hUARTx.Instance = USART3;
  hUARTx.Init.BaudRate   = 9600;
  hUARTx.Init.WordLength = UART_WORDLENGTH_8B;
  hUARTx.Init.StopBits   = UART_STOPBITS_1;
  hUARTx.Init.Parity     = UART_PARITY_NONE;
  hUARTx.Init.HwFlowCtl  = UART_HWCONTROL_NONE;
  hUARTx.Init.Mode       = UART_MODE_TX_RX;
  if(HAL_UART_DeInit(&hUARTx) != HAL_OK)
  {
    Error_Handler();
  }  
  if(HAL_UART_Init(&hUARTx) != HAL_OK)
  {
    Error_Handler();
  }
	
	HAL_NVIC_SetPriority(USART3_IRQn, 0, 0);
	HAL_NVIC_EnableIRQ(USART3_IRQn);
}

void DMA_Config(void)
{
	__HAL_RCC_DMA1_CLK_ENABLE();
	hDMA_RX.Instance = DMA1_Channel4;
	hDMA_RX.Init.Direction = DMA_PERIPH_TO_MEMORY;
	hDMA_RX.Init.PeriphInc = DMA_PINC_DISABLE;
	hDMA_RX.Init.MemInc = DMA_MINC_ENABLE;
	hDMA_RX.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
	hDMA_RX.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
	hDMA_RX.Init.Mode = DMA_CIRCULAR;
	hDMA_RX.Init.Priority = DMA_PRIORITY_MEDIUM;
	if(HAL_DMA_Init(&hDMA_RX) != HAL_OK)
	{
		Error_Handler();
	}
	
	__HAL_LINKDMA(&hUARTx, hdmarx, hDMA_RX);
	HAL_NVIC_SetPriority(DMA1_Channel4_IRQn, 0, 0);
	HAL_NVIC_EnableIRQ(DMA1_Channel4_IRQn);
	

}

/**
  * @brief  Rx Transfer completed callback
  * @param  UartHandle: UART handle
  * @note   This example shows a simple way to report end of DMA Rx transfer, and 
  *         you can add your own implementation.
  * @retval None
  */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *hu)
{
	__NOP();
  
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
