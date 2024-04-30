<!-- Items.vue -->
<template>
  <div class="calculator-item">
    <div v-if="!manualEntry">
      <div class="search-container">
        <input type="text" v-model="item.site" placeholder="Insira o link para tentar captura automática"
          class="search-input" />
        <button class="search-button" @click="searchItem">🔍</button>
      </div>
      <p @click="manualEntry = true">Clique <span class="clickable" @click="animateClick">aqui</span> para inserção
        manual</p>
    </div>
    <div v-else>
      <div class="top-row">
        <input type="text" v-model="item.title" placeholder="Componente" />
        <input type="text" v-model="item.quantity" placeholder="Qtde." class="quantity" />
        <input type="text" v-model="item.site" placeholder="Site" class="site" />
      </div>
      <div class="bottom-row">
        <input type="text" v-model="item.cashPrice" placeholder="Valor à vista" />
        <input type="text" v-model="item.installmentPrice" placeholder="Valor parcelado" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import axios from 'axios';

const props = defineProps({
  modelValue: Object
})

const emit = defineEmits(['update:modelValue'])

const item = ref(props.modelValue || {
  title: '',
  quantity: 1,
  site: '',
  cashPrice: 0,
  installmentPrice: 0
})
const manualEntry = ref(false)

watchEffect(() => {
  if (props.modelValue !== item.value) {
    item.value = { ...props.modelValue }
  }
})

watchEffect(() => {
  if (props.modelValue !== item.value) {
    emit('update:modelValue', { ...item.value })
  }
})

const searchItem = async () => {
  if (item && item.value) {
    try {
      const response = await axios.post('http://localhost:5000/search', { link: item.value.site });
      // Atualize o item com a resposta do servidor
      item.value.title = response.data.component;
      item.value.cashPrice = response.data.cash_price;
      item.value.installmentPrice = response.data.installment_price;
      item.value.quantity = 1; 

      // Switch to manual entry mode
      manualEntry.value = true;
    } catch (error) {
      console.error(error);
    }
  } else {
    console.error('item is undefined')
  }
}
</script>

<style scoped>
.calculator-item {
  display: flex;
  flex-direction: column;
  gap: 1em;
  background-color: #1a1a1a;
  padding: 1em;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  margin-bottom: 1em;
}

.calculator-item p {
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.calculator-item .clickable {
  cursor: pointer;
  text-decoration: underline;
  font-weight: bold;
  cursor: pointer;
  color: #646cff;
}

.calculator-item .top-row,
.calculator-item .bottom-row {
  display: flex;
  justify-content: space-between;
}

.calculator-item .quantity {
  width: 50px;
}

.calculator-item .site,
.calculator-item .bottom-row input {
  width: calc(70% - 1em);
}

.calculator-item input {
  padding: 0.5rem;
  width: 24rem;
  border-radius: 4px;
  border: 1px solid #646cff;
  background-color: #242424;
  color: rgba(255, 255, 255, 0.87);
}

.search-container {
  position: relative;
  width: 100%;
}

.search-input {
  padding-right: 30px;
  text-align: left;
  width: 100%;
}

.search-button {
  position: absolute;
  right: 0;
  top: 50%;
  right: 25px;
  transform: translateY(-50%);
  border: none;
  background: none;
  color: rgba(255, 255, 255, 0.87);
  cursor: pointer;
  padding: 0.5rem;
  width: 10%;
  text-align: center;
}
</style>