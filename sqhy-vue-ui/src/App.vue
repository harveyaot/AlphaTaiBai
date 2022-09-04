<script setup>
import Sents from './assets/sents.json'
import { ref, onMounted } from 'vue'
import axios from 'axios'

//let host = "http://localhost:8088"
let host = "http://192.168.0.107:8088"
let page_size = 20


const file = ref(null)
const counter = ref(0)
const message = ref("")
const hero_image = ref(host + "/static/lotus.png")
const repsonse_sents = ref(Sents)
const pageno = ref(1)
const total_page_no = ref(1)
const items = ref([1, 2, 3, 4, 5])


function handleFileUpload(event) {
  file.value = event.target.files[0];
  submitFile()
}

function submitFile() {
  let formData = new FormData();
  formData.append('file', file.value);
  // You should have a server side REST API 
  axios.post(host + '/uploadfile',
    formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }
  ).then(function (e) {
    console.log(e['data']['filename']);
    hero_image.value = host + "/uploads/" + e['data']['filename']
    axios.get(host + "/imageclf?filename=" + e['data']['filename'] + '&size=20')
      .then((res) => {
        repsonse_sents.value = res.data
      })
  })
    .catch(function () {
      console.log('FAILURE!!');
    });
}

onMounted(() => {
  axios.get(host + "/imageclf?filename=" + "/static/lotus.png" + '&size=20')
    .then((res) => {
      repsonse_sents.value = res.data
      pageno.value = res.data['page']
      total_page_no.value = res.data['total'] / res.data['size']
    })
})

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
      <div v-for="sent in repsonse_sents['items']" class="item">
        <div class="sent">{{ sent['sent'] }}</div>
        <div class="source">{{ sent['source'] }}</div>
      </div>
    </div>

    <button id="return2top" class="mdc-fab" aria-label="Favorite">
      <div class="mdc-fab__ripple"></div>
      <span class="mdc-fab__icon material-icons">arrow_upward</span>
    </button>

    <button id="pageinfo" class="mdc-fab" aria-label="Favorite">
      <div class="mdc-fab__ripple"></div>
      <span class="mdc-fab__label fraction">
        <span class="top"> {{ pageno }}</span>
        <span class="bottom"> {{ total_page_no }}</span>
      </span>
    </button>


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
