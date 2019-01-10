<template lang="html">
  <div id="app">
    <div class="container-scroller">
      <app-header/>
      <div class="container-fluid page-body-wrapper">
        <app-sidebar :username="userData.email"/>
        <div class="main-panel">
          <div class="content-wrapper">
            <router-view :userData="userData"></router-view>
          </div>
          <!-- content wrapper ends -->
          <app-footer/>
        </div>
        <!-- main panel ends -->
      </div>
      <!-- page-body-wrapper ends -->
    </div>
  </div>
</template>

<script lang="js">
import AppHeader from '../src/components/partials/AppHeader'
import AppSidebar from '../src/components/partials/AppSidebar'
import AppFooter from '../src/components/partials/AppFooter'


// setup firebase
import firebase from 'firebase'
var config = {
    apiKey: "AIzaSyCtEYxUYW_3N2ro-U-CNMVGhbXKgpN80Os",
    authDomain: "savior-42229.firebaseapp.com",
    databaseURL: "https://savior-42229.firebaseio.com",
    projectId: "savior-42229",
    storageBucket: "savior-42229.appspot.com",
    messagingSenderId: "797865036316" }
firebase.initializeApp(config)

var data = {test: 'hello'}
const self = this
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // fetch user data
    console.log(user)
    data['email'] = 'aditya@illinois.edu'
  } else {
    // No user is signed in.
    self.$router.push('login')
  }
});

export default{
  name: 'app',
  components: {
    AppHeader,
    AppSidebar,
    AppFooter
  },
  data() {
    return {userData: data}
  }
}
</script>

<style>
  @import "../node_modules/mdi/css/materialdesignicons.min.css";
  @import "../node_modules/flag-icon-css/css/flag-icon.min.css";
  @import "../node_modules/font-awesome/css/font-awesome.min.css";
</style>

<style lang="scss">
@import "./assets/scss/style";
</style>
