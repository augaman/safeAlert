import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import {
  Warning as WarningIcon,
  Group as GroupIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { useAppSelector } from '../hooks';
import { apiService } from '../services/api';
import { Alert } from '../types';

interface DashboardStats {
  totalAlerts: number;
  activeAlerts: number;
  resolvedAlerts: number;
  totalTeams: number;
}

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentAlerts, setRecentAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAppSelector((state) => state.auth);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [alerts, teams] = await Promise.all([
          apiService.getAlerts(),
          apiService.getTeamMembers(user?.teamId || ''),
        ]);

        const activeAlerts = alerts.filter((alert) => alert.status === 'pending');
        const resolvedAlerts = alerts.filter((alert) => alert.status === 'resolved');

        setStats({
          totalAlerts: alerts.length,
          activeAlerts: activeAlerts.length,
          resolvedAlerts: resolvedAlerts.length,
          totalTeams: teams.length,
        });

        setRecentAlerts(alerts.slice(0, 5));
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user?.teamId]);

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '60vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <WarningIcon color="error" sx={{ mr: 1 }} />
                <Typography variant="h6">Active Alerts</Typography>
              </Box>
              <Typography variant="h4">{stats?.activeAlerts || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Resolved Alerts</Typography>
              </Box>
              <Typography variant="h4">{stats?.resolvedAlerts || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <GroupIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Teams</Typography>
              </Box>
              <Typography variant="h4">{stats?.totalTeams || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <ErrorIcon color="warning" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Alerts</Typography>
              </Box>
              <Typography variant="h4">{stats?.totalAlerts || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Alerts */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            {recentAlerts.length > 0 ? (
              <Box>
                {recentAlerts.map((alert) => (
                  <Box
                    key={alert.id}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      py: 1,
                      borderBottom: '1px solid',
                      borderColor: 'divider',
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle1">{alert.title}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {alert.description}
                      </Typography>
                    </Box>
                    <Typography
                      variant="body2"
                      color={
                        alert.status === 'pending'
                          ? 'error'
                          : alert.status === 'resolved'
                          ? 'success'
                          : 'warning'
                      }
                    >
                      {alert.status}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="text.secondary">No recent alerts</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}; 