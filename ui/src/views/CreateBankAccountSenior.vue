<template>
  <div class="create-bank-account-senior">
    <h2>Create Bank Account for Senior</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="accountHolderName">Account Holder Name</label>
        <input type="text" id="accountHolderName" v-model="accountHolderName" name="accountHolderName" required />
      </div>
      <div>
        <label for="dateOfBirth">Date of Birth</label>
        <input type="date" id="dateOfBirth" v-model="dateOfBirth" name="dateOfBirth" required />
      </div>
      <div>
        <label for="currentAddress">Current Address</label>
        <textarea id="currentAddress" v-model="currentAddress" name="currentAddress" required></textarea>
      </div>
      <div>
        <label for="permanentAddress">Permanent Address</label>
        <input type="text" id="permanentAddress" v-model="permanentAddress" name="permanentAddress" required />
      </div>
      <div>
        <label for="sex">Sex</label>
        <input type="text" id="sex" v-model="sex" name="sex" required />
      </div>
      <div>
        <label for="annualIncome">Annual Income</label>
        <input type="number" id="annualIncome" v-model="annualIncome" name="annualIncome" required />
      </div>
      <div>
        <label for="occupation">Occupation</label>
        <input type="text" id="occupation" v-model="occupation" name="occupation" />
      </div>
      <div>
        <label for="country">Country</label>
        <select id="country" v-model="selectedCountry" required>
          <option disabled value="">Please select one</option>
          <option v-for="country in countries" :key="country.code" :value="country.name">{{ country.name }}</option>
        </select>
      </div>
      <div>
        <label for="state">State</label>
        <select id="state" v-model="selectedState" required>
          <option disabled value="">Please select one</option>
          <option v-for="state in states" :key="state">{{ state }}</option>
        </select>
      </div>
      <div>
        <label for="city">City</label>
        <input type="text" id="city" v-model="city" name="city" required />
      </div>
      <div>
        <label for="street">Street</label>
        <input type="text" id="street" v-model="street" name="street" required />
      </div>
      <div>
        <label for="pincode">Pincode</label>
        <input type="text" id="pincode" v-model="pincode" name="pincode" required />
      </div>
      <div>
        <label for="phoneNumber">Phone Number</label>
        <input type="text" id="phoneNumber" v-model="phoneNumber" name="phoneNumber" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" name="email" />
      </div>
      <div>
        <label for="photo">Photo</label>
        <input type="file" id="photo" @change="onFileChange" name="photo" />
      </div>
      <button type="submit">Create Account</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateBankAccountSenior',
  data() {
    return {
      accountHolderName: '',
      dateOfBirth: '',
      currentAddress: '',
      permanentAddress: '',
      sex: '',
      annualIncome: '',
      occupation: '',
      selectedCountry: '',
      selectedState: '',
      city: '',
      street: '',
      pincode: '',
      phoneNumber: '',
      email: '',
      photo: '',
      message: '',
      countries: [],
      states: [],
      statesData: {
        USA: ['California', 'Texas', 'Florida', 'New York'],
        India: ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu'],
        Canada: ['Ontario', 'Quebec', 'British Columbia', 'Alberta'],
        Australia: ['New South Wales', 'Victoria', 'Queensland', 'Tasmania'],
        UK: ['England', 'Scotland', 'Wales', 'Northern Ireland'],
      },
    };
  },
  created() {
    this.fetchCountries();
  },
  watch: {
    selectedCountry(newCountry) {
      this.fetchStates(newCountry);
    },
  },
  methods: {
    async fetchCountries() {
      try {
        const response = await axios.get('https://restcountries.com/v3.1/all');
        this.countries = response.data.map(country => ({
          name: country.name.common,
          code: country.cca2,
        }));
      } catch (err) {
        console.error('Error fetching countries:', err);
      }
    },
    fetchStates(countryName) {
      if (this.statesData[countryName]) {
        this.states = this.statesData[countryName];
      } else {
        this.states = [];
      }
    },
    async submitForm() {
      try {
        const response = await axios.post('/accounts/create_bank_account_senior/', {
          account_holder_name: this.accountHolderName,
          date_of_birth: this.dateOfBirth,
          current_address: this.currentAddress,
          permanent_address: this.permanentAddress,
          sex: this.sex,
          annual_income: this.annualIncome,
          occupation: this.occupation,
          country: this.selectedCountry,
          state: this.selectedState,
          city: this.city,
          street: this.street,
          pincode: this.pincode,
          phone_number: this.phoneNumber,
          email: this.email,
          photo: this.photo,
        });
        this.message = 'Account created successfully!';
      } catch (err) {
        console.error('Error creating account:', err);
        this.message = 'Failed to create bank account for senior.';
      }
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.photo = file;
    },
  },
};
</script>

<style scoped>
.create-bank-account-senior {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1em;
}

.error {
  color: red;
  margin-bottom: 1em;
}
</style>
