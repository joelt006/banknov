

 <template>
  <div class="transaction-statement">
    <h1>Transaction Statement</h1>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="transactions.length === 0" class="no-transactions">
        No transactions to display.
      </div>
      <table v-else class="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Value Date</th>
            <th>Particulars</th>
            <th>Tran Type</th>
            <th>Tran ID</th>
            <th>Sender</th>
            <th>Receiver</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ formatDate(transaction.date) }}</td>
            <td>{{ transaction.value_date ? formatDate(transaction.value_date) : 'N/A' }}</td>
            <td>{{ transaction.particulars || 'N/A' }}</td>
            <td>{{ transaction.tran_type || 'N/A' }}</td>
            <td>{{ transaction.tran_id || 'N/A' }}</td>
            <td>{{ transaction.sender || 'N/A' }}</td>
            <td>{{ transaction.receiver || 'N/A' }}</td>
            <td>${{ isNaN(Number(transaction.amount)) ? '0.00' : Number(transaction.amount).toFixed(2) }}</td>
            <td>{{ transaction.status || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TransactionStatement',
  data() {
    return {
      transactions: [], 
      loading: true,   
    };
  },
  methods: {
    async fetchTransactions() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/transactions/statement/', {
          withCredentials: true, 
        });

        this.transactions = response.data.map(transaction => ({
          ...transaction,
          amount: transaction.amount ? Number(transaction.amount) : 0, 
        }));
      } catch (error) {
        console.error('Error fetching transactions:', error);
        if (error.response) {
          console.error('Server responded with:', error.response.data);
        } else {
          console.error('Request error:', error.message);
        }
        alert('Unable to fetch transaction statements.');
      } finally {
        this.loading = false; 
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
  created() {
    this.fetchTransactions();
  },
};
</script>

<style scoped>
.transaction-statement {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #070707;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(175, 173, 173, 0.1);
  background-color: #0d0d0d;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.loading {
  text-align: center;
  font-size: 18px;
}

.no-transactions {
  text-align: center;
  font-size: 16px;
  color: #0d0d0d;
}

.transaction-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.transaction-table th,
.transaction-table td {
  border: 1px solid #050505;
  padding: 10px;
  text-align: left;
}

.transaction-table th {
  background-color: #0e0d0d;
  color: #333;
}

.transaction-table tbody tr:nth-child(even) {
  background-color: #111111;
}

.transaction-table tbody tr:hover {
  background-color: #0d0d0d;
}

.transaction-table td {
  font-size: 14px;
}

.transaction-table th {
  font-size: 16px;
}
</style>

