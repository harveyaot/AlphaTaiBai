<script setup>
import Sents from './assets/sents.json'
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const counter = ref(0)
const message = ref("")
const hero_image = ref("/src/assets/lotus.png")
const repsonse_sents = ref(Sents)

function handleFileUpload(event) {
  file.value = event.target.files[0];
  submitFile()
}

function submitFile() {
  let formData = new FormData();
  formData.append('file', file.value);
  // You should have a server side REST API 
  axios.post('http://localhost:8088/uploadfile',
    formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }
  ).then(function (e) {
    console.log(e['data']['filename']);
    hero_image.value = "http://localhost:8088/uploads/" + e['data']['filename']
    axios.get("http://localhost:8088/imageclf?filename=" + e['data']['filename'])
    .then((res) => {
        repsonse_sents.value = res.data 
    })
  })
    .catch(function () {
      console.log('FAILURE!!');
    });
}

</script>

<template>
  <section>
    <div id="hero-img">
      <div><img :src="hero_image" alt=""></div>
      <div class="mdc-touch-target-wrapper upload-btn">
        <label for="uploadfile1" class="mdc-fab mdc-fab--mini mdc-fab--touch">
          <div class="mdc-fab__ripple"></div>
          <span class="material-icons mdc-fab__icon">add</span>
          <div class="mdc-fab__touch"></div>
          <input id="uploadfile1" type="file" @change="handleFileUpload($event)" />
        </label>
      </div>
    </div>
    <div class="result">
      <div v-for="sent in repsonse_sents['results']" class="item">
        <div class="sent">{{ sent['sent'] }}</div>
        <div class="source">{{ sent['source'] }}</div>
      </div>
    </div>

    <div class="pagination">
      <!--before page-->
      <svg xmlns="http://www.w3.org/2000/svg" height="48" width="48">
        <path d="M28.05 36 16 23.95 28.05 11.9l2.15 2.15-9.9 9.9 9.9 9.9Z" />
      </svg>

      <!--next-->
      <svg xmlns="http://www.w3.org/2000/svg" height="48" width="48">
        <path d="m18.75 36-2.15-2.15 9.9-9.9-9.9-9.9 2.15-2.15L30.8 23.95Z" />
      </svg>
    </div>

  </section>
</template>

<style>
@import './assets/main.css';
</style>
