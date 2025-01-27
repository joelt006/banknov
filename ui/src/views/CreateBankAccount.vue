<template>
  <div>
    <h1>Create Bank Account</h1>
    <form @submit.prevent="createAccount">
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
        <input type="text" id="country" v-model="country" name="country" required />
      </div>
      <div>
        <label for="state">State</label>
        <input type="text" id="state" v-model="state" name="state" required />
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
        <label for="aadharNumber">Aadhar Number</label>
        <input type="text" id="aadharNumber" v-model="aadharNumber" name="aadharNumber" />
      </div>
      <div>
        <label for="passportNumber">Passport Number</label>
        <input type="text" id="passportNumber" v-model="passportNumber" name="passportNumber" />
      </div>
      <div>
        <label for="voterIdNumber">Voter ID Number</label>
        <input type="text" id="voterIdNumber" v-model="voterIdNumber" name="voterIdNumber" />
      </div>
      <div>
        <label for="panCardNumber">PAN Card Number</label>
        <input type="text" id="panCardNumber" v-model="panCardNumber" name="panCardNumber" />
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
export default {
  data() {
    return {
      accountHolderName: '',
      dateOfBirth: '',
      currentAddress: '',
      permanentAddress: '',
      sex: '',
      annualIncome: 0,
      occupation: '',
      country: 'India',
      state: 'Kerala',
      city: 'Delhi',
      street: 'Main Lane',
      pincode: '123456',
      phoneNumber: '',
      email: '',
      aadharNumber: '',
      passportNumber: '',
      voterIdNumber: '',
      panCardNumber: '',
      photo: null,
      message: ''
    };
  },
  methods: {
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    onFileChange(event) {
      this.photo = event.target.files[0];
    },
    async createAccount() {
      const formData = new FormData();
      formData.append('account_holder_name', this.accountHolderName);
      formData.append('date_of_birth', this.dateOfBirth);
      formData.append('current_address', this.currentAddress);
      formData.append('permanent_address', this.permanentAddress); // Fixed key here
      formData.append('sex', this.sex);
      formData.append('annual_income', this.annualIncome);
      formData.append('occupation', this.occupation);
      formData.append('country', this.country);
      formData.append('state', this.state);
      formData.append('city', this.city);
      formData.append('street', this.street);
      formData.append('pincode', this.pincode);
      formData.append('phone_number', this.phoneNumber);
      formData.append('email', this.email);
      formData.append('aadhar_number', this.aadharNumber);
      formData.append('passport_number', this.passportNumber);
      formData.append('voter_id_number', this.voterIdNumber);
      formData.append('pan_card_number', this.panCardNumber);
      formData.append('photo', this.photo);

      const csrfToken = this.getCookie('csrftoken');

      try {
        const response = await fetch('http://127.0.0.1:8000/accounts/CreateBankAccount/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          body: formData
        });



        if (response.ok) {
          const text = await response.text();  // Read the response as text

          this.message = `Error: ${text}`;  // Set message based on raw text
          console.error("Error response body:", text);
          return;
        } 

        const data = await response.json();  // Read the response as JSON
        this.message = 'Account created successfully!';
      } catch (error) {
        this.message = `Error: ${error.message}`;
        console.error('Error creating account:', error);
      }
    }
  }
};
</script>

<style scoped>
.create-bank-account {
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
