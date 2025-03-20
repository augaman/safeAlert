import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import { RootState } from '../store';
import { fetchAlerts } from '../store/slices/alertsSlice';
import { Alert, Team } from '../types';

const DashboardScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { alerts, loading } = useSelector((state: RootState) => state.alerts);
  const { user } = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    dispatch(fetchAlerts());
  }, [dispatch]);

  const activeAlerts = alerts.filter((alert) => alert.status !== 'resolved');
  const criticalAlerts = alerts.filter((alert) => alert.severity === 'critical');
  const availableTeams = 0; // TODO: Implement team status tracking

  const StatCard: React.FC<{
    title: string;
    value: number | string;
    color: string;
  }> = ({ title, value, color }) => (
    <Paper
      sx={{
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        height: 140,
        backgroundColor: color,
        color: 'white',
      }}
    >
      <Typography component="h2" variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography component="p" variant="h4">
        {value}
      </Typography>
    </Paper>
  );

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Welcome back, {user?.name}
          </Typography>
        </Grid>
        <Grid item xs={12} md={4}>
          <StatCard
            title="Active Alerts"
            value={activeAlerts.length}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <StatCard
            title="Critical Alerts"
            value={criticalAlerts.length}
            color="#d32f2f"
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <StatCard
            title="Available Teams"
            value={availableTeams}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            {activeAlerts.length === 0 ? (
              <Typography>No active alerts</Typography>
            ) : (
              <Box>
                {activeAlerts.slice(0, 5).map((alert) => (
                  <Box
                    key={alert.id}
                    sx={{
                      p: 2,
                      mb: 1,
                      borderBottom: '1px solid #eee',
                    }}
                  >
                    <Typography variant="subtitle1">
                      {alert.type.charAt(0).toUpperCase() + alert.type.slice(1)} Alert
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {alert.description}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(alert.createdAt).toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default DashboardScreen; 