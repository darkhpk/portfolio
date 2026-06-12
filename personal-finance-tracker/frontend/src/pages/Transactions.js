import React from 'react';
import { Container, Typography } from '@mui/material';

function Transactions() {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        Transactions
      </Typography>
      <Typography>
        Transaction management interface - to be implemented with full CRUD operations
      </Typography>
    </Container>
  );
}

export default Transactions;
