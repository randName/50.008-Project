<template>
<v-container fluid>
  <v-alert v-for="e in errors" :key="e" type="error" value="true">
    {{ e }}
  </v-alert>
  <v-form v-model="valid" ref="form" @input="clearerr" lazy-validation>
    <v-text-field required
      v-model="form.username"
      name="username"
      label="Username"
      :rules="reqRule"
    ></v-text-field>
    <v-text-field required
      v-model="form.password"
      name="password"
      label="Password"
      :rules="reqRule"
      :type="pwtype" :append-icon="pwicon" :append-icon-cb="togglepw"
    ></v-text-field>
    <v-text-field v-if="register" required
      v-model="form.password2"
      name="password2"
      label="Password Confirmation"
      :rules="comRule"
      :type="pwtype" :append-icon="pwicon" :append-icon-cb="togglepw"
    ></v-text-field>
    <v-btn @click="login" :disabled="!valid">{{ actiontext }}</v-btn>
    <v-btn @click="register=!register">{{ switchtext }}</v-btn>
  </v-form>
</v-container>
</template>

<script>
export default {
  methods: {
    clearerr () {
      this.errors = []
    },
    login () {
      if (this.$refs.form.validate()) {
        this.$user.login(this.form, this.register)
        .then(() => this.$router.push('/'))
        .catch(e => this.errors = e.response.data.messages)
      }
    },
    matchpw (p) {
      return !this.register || this.form.password == p
    },
    togglepw () {
      this.pw = !this.pw
    }
  },
  computed: {
    pwtype () {
      return this.pw ? 'password' : 'text'
    },
    pwicon () {
      return this.pw ? 'visibility' : 'visibility_off'
    },
    actiontext () {
      return this.register ? 'Register' : 'Login'
    },
    switchtext () {
      return this.register ? 'Got Account Liao' : 'Register'
    }
  },
  data () {
    return {
      form: {
        username: '',
        password: '',
        password2: ''
      },
      errors: [],
      reqRule: [(v) => !!v || 'This field is required'],
      comRule: [(v) => this.matchpw(v) || 'Passwords do not match'],
      pw: true,
      valid: true,
      register: false
    }
  }
}
</script>
