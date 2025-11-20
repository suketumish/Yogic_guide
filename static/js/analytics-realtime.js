/**
 * Real-time Analytics Update System
 * Polls the server every 30 seconds for updated analytics data
 * and dynamically updates all charts without page refresh
 */

// Store chart instances globally for updates
let chartInstances = {};
let updateInterval = null;
let isUpdating = false;

/**
 * Initialize real-time updates
 * @param {number} intervalSeconds - Update interval in seconds (default: 30)
 */
function initializeRealTimeUpdates(intervalSeconds = 30) {
    console.log(`🔄 Initializing real-time analytics updates (every ${intervalSeconds}s)`);
    
    // Start polling
    updateInterval = setInterval(() => {
        fetchAndUpdateAnalytics();
    }, intervalSeconds * 1000);
    
    // Also update on visibility change (when user returns to tab)
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            console.log('👁️ Tab visible - refreshing analytics');
            fetchAndUpdateAnalytics();
        }
    });
}

/**
 * Fetch latest analytics data from API and update all charts
 */
async function fetchAndUpdateAnalytics() {
    // Prevent concurrent updates
    if (isUpdating) {
        console.log('⏳ Update already in progress, skipping...');
        return;
    }
    
    isUpdating = true;
    showLoadingIndicator();
    
    try {
        console.log('📊 Fetching live analytics data...');
        const response = await fetch('/api/analytics/live');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Analytics data received:', data);
        
        // Update all components
        updateMetricsCards(data.metrics);
        updateCharts(data);
        updateLastRefreshTime();
        
        console.log('✅ Analytics updated successfully');
        
    } catch (error) {
        console.error('❌ Error fetching analytics:', error);
        showErrorNotification('Failed to update analytics. Will retry in 30 seconds.');
    } finally {
        isUpdating = false;
        hideLoadingIndicator();
    }
}

/**
 * Update metric cards with new data
 */
function updateMetricsCards(metrics) {
    // Update each metric card with smooth animation
    const metricUpdates = [
        { selector: '.gradient-card:nth-child(1) .text-3xl', value: metrics.totalUsers },
        { selector: '.gradient-card:nth-child(2) .text-3xl', value: metrics.totalSessions },
        { selector: '.gradient-card:nth-child(3) .text-3xl', value: metrics.activeUsers7d },
        { selector: '.bg-gradient-to-r.from-orange-500 .text-3xl', value: metrics.avgSessionDuration },
        { selector: '.bg-gradient-to-r.from-pink-500 .text-3xl', value: `${metrics.retentionRate}%` },
        { selector: '.bg-gradient-to-r.from-indigo-500 .text-3xl', value: metrics.activeUsers30d }
    ];
    
    metricUpdates.forEach(update => {
        const element = document.querySelector(update.selector);
        if (element) {
            animateValue(element, update.value);
        }
    });
}

/**
 * Animate value change in metric cards
 */
function animateValue(element, newValue) {
    const currentValue = element.textContent;
    
    // Add pulse animation
    element.style.transition = 'transform 0.3s ease';
    element.style.transform = 'scale(1.1)';
    
    setTimeout(() => {
        element.textContent = newValue;
        element.style.transform = 'scale(1)';
    }, 150);
}

/**
 * Update all charts with new data
 */
function updateCharts(data) {
    // Update User Growth Chart
    if (chartInstances.userGrowth) {
        chartInstances.userGrowth.data.labels = data.userGrowth.labels;
        chartInstances.userGrowth.data.datasets[0].data = data.userGrowth.data;
        chartInstances.userGrowth.update('none'); // 'none' for no animation
    }
    
    // Update Session Analytics Chart
    if (chartInstances.sessionAnalytics) {
        chartInstances.sessionAnalytics.data.labels = data.sessionAnalytics.labels;
        chartInstances.sessionAnalytics.data.datasets[0].data = data.sessionAnalytics.sessions;
        chartInstances.sessionAnalytics.data.datasets[1].data = data.sessionAnalytics.durations;
        chartInstances.sessionAnalytics.update('none');
    }
    
    // Update Module Performance Chart
    if (chartInstances.modulePerformance) {
        chartInstances.modulePerformance.data.labels = data.modulePerformance.labels;
        chartInstances.modulePerformance.data.datasets[0].data = data.modulePerformance.data;
        chartInstances.modulePerformance.update('none');
    }
    
    // Update Accuracy Distribution Chart
    if (chartInstances.accuracyDistribution) {
        chartInstances.accuracyDistribution.data.datasets[0].data = data.accuracyDistribution.data;
        chartInstances.accuracyDistribution.update('none');
    }
    
    // Update Platform Health Gauge
    if (chartInstances.platformHealth) {
        const healthScore = data.platformHealth.score;
        chartInstances.platformHealth.data.datasets[0].data = [healthScore, 100 - healthScore];
        chartInstances.platformHealth.update('none');
    }
    
    // Update User Engagement Chart
    if (chartInstances.userEngagement) {
        chartInstances.userEngagement.data.labels = data.userEngagement.labels;
        chartInstances.userEngagement.data.datasets[0].data = data.userEngagement.data;
        chartInstances.userEngagement.update('none');
    }
    
    // Update Hourly Usage Chart
    if (chartInstances.hourlyUsage) {
        const hourlyData = [];
        for (let hour = 0; hour < 24; hour++) {
            hourlyData.push(data.hourlyUsage[hour] || 0);
        }
        chartInstances.hourlyUsage.data.datasets[0].data = hourlyData;
        chartInstances.hourlyUsage.update('none');
    }
    
    // Update Weekly Trends Chart
    if (chartInstances.weeklyTrends) {
        const weeklyData = [];
        for (let day = 1; day <= 7; day++) {
            weeklyData.push(data.weeklyTrends[day] || 0);
        }
        chartInstances.weeklyTrends.data.datasets[0].data = weeklyData;
        chartInstances.weeklyTrends.update('none');
    }
    
    // Update Retention Chart
    if (chartInstances.retention) {
        chartInstances.retention.data.labels = data.retention.labels;
        chartInstances.retention.data.datasets[0].data = data.retention.data;
        chartInstances.retention.update('none');
    }
}

/**
 * Show loading indicator during updates
 */
function showLoadingIndicator() {
    // Create or show loading indicator
    let indicator = document.getElementById('analytics-loading-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'analytics-loading-indicator';
        indicator.className = 'fixed top-4 right-4 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 flex items-center space-x-2';
        indicator.innerHTML = `
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Updating analytics...</span>
        `;
        document.body.appendChild(indicator);
    } else {
        indicator.style.display = 'flex';
    }
}

/**
 * Hide loading indicator
 */
function hideLoadingIndicator() {
    const indicator = document.getElementById('analytics-loading-indicator');
    if (indicator) {
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 500);
    }
}

/**
 * Show error notification
 */
function showErrorNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg z-50';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Update last refresh time display
 */
function updateLastRefreshTime() {
    let timeDisplay = document.getElementById('last-refresh-time');
    
    if (!timeDisplay) {
        // Create time display element
        timeDisplay = document.createElement('div');
        timeDisplay.id = 'last-refresh-time';
        timeDisplay.className = 'text-sm text-gray-500 mt-2';
        
        // Insert after the header
        const header = document.querySelector('.welcome-animation');
        if (header) {
            header.appendChild(timeDisplay);
        }
    }
    
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    timeDisplay.textContent = `Last updated: ${timeString}`;
}

/**
 * Stop real-time updates (cleanup)
 */
function stopRealTimeUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
        console.log('🛑 Real-time updates stopped');
    }
}

/**
 * Manual refresh function (called by refresh button)
 */
function manualRefresh() {
    console.log('🔄 Manual refresh triggered');
    fetchAndUpdateAnalytics();
}

// Export functions for global access
window.initializeRealTimeUpdates = initializeRealTimeUpdates;
window.stopRealTimeUpdates = stopRealTimeUpdates;
window.manualRefresh = manualRefresh;
window.chartInstances = chartInstances;
