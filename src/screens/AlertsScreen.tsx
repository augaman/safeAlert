import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Box,
  CircularProgress,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  TextField,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import { MoreVert as MoreVertIcon } from '@mui/icons-material';
import { RootState } from '../store';
import { fetchAlerts, updateAlertStatus } from '../store/slices/alertsSlice';
import { Alert, AlertFilters } from '../types';

const AlertsScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { alerts, loading } = useSelector((state: RootState) => state.alerts);
  const [filters, setFilters] = useState<AlertFilters>({});
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);

  useEffect(() => {
    dispatch(fetchAlerts(filters));
  }, [dispatch, filters]);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, alert: Alert) => {
    setAnchorEl(event.currentTarget);
    setSelectedAlert(alert);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedAlert(null);
  };

  const handleStatusUpdate = async (status: Alert['status']) => {
    if (!selectedAlert) return;

    try {
      await dispatch(
        updateAlertStatus({
          id: selectedAlert.id,
          alertId: selectedAlert.id,
          teamId: selectedAlert.assignedTeamId || '',
          status,
          message: `Status updated to ${status}`,
          timestamp: new Date().toISOString(),
        })
      );
      handleMenuClose();
    } catch (error) {
      console.error('Failed to update alert status:', error);
    }
  };

  const getSeverityColor = (severity: Alert['severity']) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: Alert['status']) => {
    switch (status) {
      case 'pending':
        return 'default';
      case 'assigned':
        return 'info';
      case 'in_progress':
        return 'warning';
      case 'resolved':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

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
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Alerts
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Type</InputLabel>
            <Select
              value={filters.type || ''}
              label="Type"
              onChange={(e) => setFilters({ ...filters, type: e.target.value as Alert['type'] })}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="fire">Fire</MenuItem>
              <MenuItem value="flood">Flood</MenuItem>
              <MenuItem value="earthquake">Earthquake</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Severity</InputLabel>
            <Select
              value={filters.severity || ''}
              label="Severity"
              onChange={(e) => setFilters({ ...filters, severity: e.target.value as Alert['severity'] })}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="critical">Critical</MenuItem>
              <MenuItem value="high">High</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="low">Low</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={filters.status || ''}
              label="Status"
              onChange={(e) => setFilters({ ...filters, status: e.target.value as Alert['status'] })}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="pending">Pending</MenuItem>
              <MenuItem value="assigned">Assigned</MenuItem>
              <MenuItem value="in_progress">In Progress</MenuItem>
              <MenuItem value="resolved">Resolved</MenuItem>
              <MenuItem value="cancelled">Cancelled</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alerts.map((alert) => (
              <TableRow key={alert.id}>
                <TableCell>{alert.type}</TableCell>
                <TableCell>{alert.description}</TableCell>
                <TableCell>
                  <Chip
                    label={alert.severity}
                    color={getSeverityColor(alert.severity)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={alert.status}
                    color={getStatusColor(alert.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {new Date(alert.createdAt).toLocaleString()}
                </TableCell>
                <TableCell>
                  <IconButton
                    size="small"
                    onClick={(e) => handleMenuClick(e, alert)}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleStatusUpdate('assigned')}>
          Assign
        </MenuItem>
        <MenuItem onClick={() => handleStatusUpdate('in_progress')}>
          Start Progress
        </MenuItem>
        <MenuItem onClick={() => handleStatusUpdate('resolved')}>
          Mark as Resolved
        </MenuItem>
        <MenuItem onClick={() => handleStatusUpdate('cancelled')}>
          Cancel
        </MenuItem>
      </Menu>
    </Container>
  );
};

export default AlertsScreen; 