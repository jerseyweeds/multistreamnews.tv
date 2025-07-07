# Google Analytics Dashboard Setup Guide

**Multi Stream News .TV - Analytics Dashboard Configuration**

*Created: July 3, 2025*  
*For use with: analytics.google.com/analytics/web*

## Overview

This guide provides step-by-step instructions for setting up custom dashboards and reports in Google Analytics to monitor visitor session numbers and other key metrics for Multi Stream News .TV.

## 1. Creating Custom Dashboards

### Navigate to Dashboards:
1. Go to **analytics.google.com/analytics/web**
2. Select your **Multi Stream News .TV** property
3. In the left sidebar, click **Reports** → **Library**
4. Click **Create new report** or **Create collection**

### Create a Custom Dashboard:
1. Click **"Create new report"**
2. Choose **"Blank report"** or **"Detail report"**
3. Name it something like "Multi Stream News Session Analytics"

## 2. Adding Session Metrics

### Key Metrics to Add:
```
Primary Metrics:
- Sessions
- Users  
- New users
- Engaged sessions
- Average engagement time
- Pages per session
- Bounce rate

Secondary Metrics:
- Session conversion rate
- Revenue per session (if e-commerce enabled)
- Goal completions per session
- Events per session
```

### Steps to Add Metrics:
1. In your custom report, click **"Add metric"**
2. Search for and select:
   - **Sessions** (total sessions)
   - **Users** (unique users)
   - **New users** (first-time visitors)
   - **Engaged sessions** (sessions longer than 10 seconds)
   - **Average engagement time**
   - **Engagement rate**

## 3. Adding Useful Dimensions

### Recommended Dimensions:
```
Time-based:
- Date
- Hour
- Day of week
- Month

Traffic Sources:
- Default channel grouping
- Source/medium
- Campaign
- Landing page

User Behavior:
- Device category
- Browser
- Operating system
- Country
- City
```

### To Add Dimensions:
1. Click **"Add dimension"**
2. Select from categories like:
   - **Time** → Date, Hour, Day of week
   - **Technology** → Device category, Browser
   - **Geography** → Country, City
   - **Acquisition** → Source/medium, Campaign

## 4. Creating Specific Session Reports

### Daily Session Trends:
- **Metric**: Sessions, Users
- **Dimension**: Date
- **Date range**: Last 30 days
- **Visualization**: Line chart

### Device Session Breakdown:
- **Metric**: Sessions, Engagement rate
- **Dimension**: Device category
- **Visualization**: Pie chart or bar chart

### Hourly Session Activity:
- **Metric**: Sessions, Active users
- **Dimension**: Hour
- **Visualization**: Bar chart

## 5. Setting Up Real-time Session Monitoring

### Access Real-time Reports:
1. Go to **Reports** → **Realtime**
2. View current active users
3. See real-time sessions by:
   - Device
   - Location  
   - Traffic source
   - Page

### Create Real-time Dashboard Widget:
1. In **Realtime** section
2. Click **"Add to dashboard"** on any real-time report
3. Customize the time window (last 30 minutes)

## 6. Advanced Session Analysis

### Create Cohort Analysis:
1. Go to **Reports** → **Retention** → **Cohort exploration**
2. Set up user cohorts based on first session date
3. Track return sessions over time

### Session Quality Segments:
Create **Audience segments** for:
- High-engagement sessions (>2 minutes)
- Multi-page sessions (>1 page)
- Return visitors
- Mobile vs Desktop sessions

### Steps to Create Segments:
1. Click **"Add comparison"** in any report
2. Select **"Create new segment"**
3. Define conditions like:
   - Session duration > 120 seconds
   - Page views per session > 1
   - User type = Returning visitor

## 7. Setting Up Automated Reports

### Schedule Email Reports:
1. In any custom report, click **"Share"**
2. Select **"Schedule email"**
3. Set frequency (daily, weekly, monthly)
4. Choose recipients
5. Include session metrics summary

### Export Options:
- **PDF**: For executive summaries
- **CSV**: For detailed analysis
- **Google Sheets**: For live data connection

## 8. Creating Alerts for Session Changes

### Set Up Intelligence Alerts:
1. Go to **Admin** → **Custom Alerts**
2. Create alerts for:
   - Sessions decrease by >20%
   - Session duration drops significantly
   - Bounce rate increases above threshold
3. Get email notifications for unusual session patterns

## 9. Recommended Dashboard Layout

### Suggested Dashboard Structure:
```
Top Row: Key Session Metrics
- Total Sessions (last 30 days)
- Average Sessions per day
- Session growth rate
- Engagement rate

Middle Row: Session Breakdown
- Sessions by device type (pie chart)
- Sessions by traffic source (bar chart)
- Session duration distribution

Bottom Row: Trends
- Daily sessions trend (line chart)
- Hourly session activity (bar chart)
- Weekly session comparison
```

## 10. Mobile App for Monitoring

### Google Analytics Mobile App:
1. Download **Google Analytics** app
2. Sign in with your account
3. Access real-time session data
4. Set up push notifications for alerts
5. View session summaries on-the-go

## 11. Integration with Multi Stream News .TV

### Current Analytics Implementation:
The site already includes GA4 tracking with custom events:

```javascript
// Video interaction tracking
gtag('event', 'video_add', {
  'custom_parameter_1': 'news_channel'
});

// Engagement milestone tracking
gtag('event', 'engagement_milestone', {
  'visit_count': visitCount
});

// Video management actions
gtag('event', 'video_maximize');
gtag('event', 'video_minimize');
gtag('event', 'bulk_add_networks');
```

### Recommended Custom Goals:
1. **Engaged Session**: User adds at least one video
2. **Power User**: User adds 3+ videos in one session
3. **Return Visitor**: User visits site multiple times
4. **Video Engagement**: User maximizes/minimizes videos

## 12. API Integration Options

### For Advanced Dashboard Integration:
- **Google Analytics Reporting API v4**: Access historical data
- **Google Analytics 4 Data API**: Access GA4 specific metrics
- **Real-time Reporting API**: Get current active sessions
- **Management API**: Automate report creation

### Authentication Methods:
- **OAuth 2.0**: For client-side applications
- **Service Account**: For server-side applications
- **API Keys**: For public data access

## Quick Setup Checklist

- [ ] Create custom dashboard in GA4
- [ ] Add key session metrics (Sessions, Users, Engagement time)
- [ ] Set up device category dimension
- [ ] Create real-time session monitoring widget
- [ ] Schedule weekly email reports
- [ ] Set up session decrease alerts
- [ ] Create segments for high-engagement users
- [ ] Export baseline data for comparison
- [ ] Install GA mobile app for monitoring
- [ ] Document custom event tracking

## Troubleshooting

### Common Issues:
1. **Data not appearing**: Check GA4 property selection
2. **Metrics unavailable**: Verify GA4 vs Universal Analytics
3. **Real-time data missing**: Confirm tracking code implementation
4. **Export failures**: Check permissions and data freshness

### Support Resources:
- [Google Analytics Help Center](https://support.google.com/analytics)
- [GA4 Migration Guide](https://support.google.com/analytics/answer/9744165)
- [Custom Report Builder Documentation](https://support.google.com/analytics/answer/1033013)

---

**Last Updated**: July 3, 2025  
**Created for**: Multi Stream News .TV Analytics  
**Next Review**: August 2025
