import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js';
import { CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend, LineController, Filler } from 'chart.js';

Chart.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend, LineController, Filler);

const StockGraph = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    console.log("Data received:", data); // Log the received props

    if (chartRef.current && data) {
      const { dates, stock_prices } = data;

      // Check if dates and stock_prices are available and valid
      if (Array.isArray(dates) && Array.isArray(stock_prices) && dates.length > 0 && stock_prices.length > 0) {
        const ctx = chartRef.current.getContext('2d');

        // Flatten the stock_prices to ensure it's just a list of numbers
        const flattenedPrices = stock_prices.map(priceArray => priceArray[0]);

        console.log("Flattened Prices:", flattenedPrices); // Log flattened prices

        const combinedData = dates.map((date, index) => ({
          date: date,
          stock_price: flattenedPrices[index],
        }));

        console.log("Combined Data:", combinedData); // Log combined data to ensure it's correct

        const chartDates = combinedData.map(item => item.date);
        const prices = combinedData.map(item => item.stock_price);

        // Ensure all prices are valid numbers
        const invalidPrices = prices.filter(price => isNaN(price));
        if (invalidPrices.length > 0) {
          console.error("Invalid prices detected:", invalidPrices);
        }

        // Check if the data is being passed correctly
        console.log("Chart Dates:", chartDates);
        console.log("Prices:", prices);

        if (chartRef.current.chart) {
          chartRef.current.chart.destroy();
        }

        const chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: chartDates,
            datasets: [{
              label: 'Stock Price',
              data: prices,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              fill: true,
              tension: 0.1
            }]
          },
          options: {
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: 'Stock Price Over Time'
              },
              tooltip: {
                mode: 'index',
                intersect: false
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Date'
                },
                ticks: {
                  autoSkip: true,
                  maxRotation: 90,
                  minRotation: 45
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Stock Price'
                },
                beginAtZero: false,
                suggestedMin: Math.min(...prices) * 0.95,
                suggestedMax: Math.max(...prices) * 1.05,
              }
            }
          }
        });

        chartRef.current.chart = chartInstance;
      } else {
        console.error("Invalid data format or missing data: dates or stock_prices are not valid.");
      }
    }

    return () => {
      if (chartRef.current && chartRef.current.chart) {
        chartRef.current.chart.destroy();
      }
    };
  }, [data]);

  return (
    <div className="stock-graph">
      <h3>Stock Price Over Time</h3>
      {data && data.dates && data.stock_prices ? (
        <canvas ref={chartRef} width={600} height={400} /> // Set canvas width and height explicitly for testing
      ) : (
        <p>Loading graph data...</p>
      )}
    </div>
  );
};

export default StockGraph;
