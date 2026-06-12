import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box } from '@mui/material';
import { reportService } from '../services/api';

function Dashboard() {
  const [summary, setSummary] = useState({
    total_income: 0,
    total_expenses: 0,
    balance: 0,
    transaction_count: 0
  });

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const response = await reportService.getSummary();
      setSummary(response.data);
    } catch (err) {
      console.error('Failed to load summary', err);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="textSecondary" gutterBottom>
              Total Income
            </Typography>
            <Typography variant="h4" color="success.main">
              ${summary.total_income.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="textSecondary" gutterBottom>
              Total Expenses
            </Typography>
            <Typography variant="h4" color="error.main">
              ${summary.total_expenses.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="textSecondary" gutterBottom>
              Balance
            </Typography>
            <Typography variant="h4" color={summary.balance >= 0 ? 'success.main' : 'error.main'}>
              ${summary.balance.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography color="textSecondary" gutterBottom>
              Transactions
            </Typography>
            <Typography variant="h4">
              {summary.transaction_count}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;
