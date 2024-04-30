<template>
  <div class="app">
    <div class="left">
      <h2>Items</h2>
      <div class="items-container">
        <div class="items">
          <CalculatorItem v-for="(item, index) in items" :key="index" :modelValue="items[index]"
            @update:modelValue="newItem => updateItem(index, newItem)" />
        </div>
      </div>
      <div class="buttons">
        <button @click="addItem">+</button>
        <button @click="removeItem">-</button>
      </div>
    </div>
    <div class="right">
      <Subtotals :items="items" />
      <Results :items="items" :subtotals="subtotals" />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import CalculatorItem from './components/Items.vue'
import Subtotals from './components/Subtotals.vue'
import Results from './components/Results.vue'

const items = ref([])
const addItem = () => {
  items.value.push({
    title: '',
    quantity: 0,
    site: '',
    cashPrice: 0,
    installmentPrice: 0
  })
  nextTick(() => {
    const container = document.querySelector('.items')
    container.scrollTop = container.scrollHeight
  })
}

const removeItem = () => {
  items.value.pop()
}

const updateItem = (index, newItem) => {
  items.value[index] = newItem
}

const componentNames = {
  'Placa Mãe': 'Placa Mãe',
  'Processador': 'Processador',
  'Memória RAM': 'Memória RAM',
  'Disco Rígido': 'Disco Rígido',
  'SSD': 'SSD',
  'Placa de Vídeo': 'Placa de Vídeo',
  'Fonte': 'Fonte de Alimentação',
  'Cooler': 'Cooler',
  'Gabinete': 'Gabinete',
  'Monitor': 'Monitor',
  'Teclado': 'Teclado',
  'Mouse': 'Mouse',
  'Headset': 'Headset',
  'Placa de Rede': 'Placa de Rede',
  'Placa de Som': 'Placa de Som'
}

// Compute subtotals based on items
const subtotals = computed(() => {
  return items.value.map(item => {
    return {
      ...item,
      component: componentNames[item.component] || item.component,
      subtotalCash: item.quantity * item.cashPrice,
      subtotalInstallment: item.quantity * item.installmentPrice
    }
  })
})

const totalCash = computed(() => {
  return subtotals.value.reduce((total, item) => total + item.subtotalCash, 0)
})

const totalInstallment = computed(() => {
  return subtotals.value.reduce((total, item) => total + item.subtotalInstallment, 0)
})
</script>
<style scoped>
.app {
  display: flex;
  justify-content: center;
  align-items: start;
  height: 100vh;
  width: 100vw;
  background-color: hsl(0, 0%, 14%);
}

.left h2 {
  padding-top: 0;
  padding-bottom: 0.5rem;
  margin-top: 0;
  margin-bottom: 0;
}

.left,
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.items-container {
  display: flex;
  flex-direction: column;
  gap: 1em;
  background-color: #1a1a1a;
  padding: 1em;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  margin-bottom: 1em;
  max-width: 500px;
  width: 100%;
  height: 890px;
  max-height: calc(5 * 70px);
  scrollbar-width: none;
  overflow: overlay;
  overflow-y: overlay;
}

/* Para navegadores baseados em WebKit */
.items-container::-webkit-scrollbar {
  display: none;
  /* Isso esconde a barra de rolagem */
}

.left .items {
  max-height: calc(5 * 88px);
  margin-bottom: 1rem;
}

.left .items::-webkit-scrollbar {
  width: 0px;
}

.left .items::-webkit-scrollbar-track {
  background: #444;
  border-radius: 4px;
}

.left .items::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.left .buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.right>* {
  flex: 1;
}
</style>