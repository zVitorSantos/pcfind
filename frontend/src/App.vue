<template>
  <div class="app">
    <div class="left">
      <h2>Items</h2>
      <div class="items-container">
        <div class="items">
          <CalculatorItem v-for="(item, index) in items" :key="index" :modelValue="items[index]"
            @update:modelValue="newItem => updateItem(index, newItem)" />
          <div class="spacer"></div>
        </div>
      </div>
      <div class="buttons">
        <button @click="addItem">+</button>
        <button @click="removeItem">-</button>
      </div>
    </div>
    <div class="right">
      <Subtotals :items="items" @update:selectedPriceType="handleUpdateSelectedPriceType"
        @updateTotals="updateTotals" />
      <Results :totalCash="totalCash" :totalInstallment="totalInstallment" :selectedTotal="selectedTotal"
        :subtotals="subtotals" :items="items" />
    </div>
  </div>
  <div class="footer">
    <ComputerParts :subtotals="subtotals" />
    <LatestAdditions />
    <Contacts />
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import CalculatorItem from './components/Items.vue';
import Subtotals from './components/Subtotals.vue';
import Results from './components/Results.vue';

// Importando os componentes do rodapé
import ComputerParts from './components/Footer/ComputerParts.vue';
import LatestAdditions from './components/Footer/LatestAdditions.vue';
import Contacts from './components/Footer/Contacts.vue';

const items = ref([])
const totalCash = ref(0)
const totalInstallment = ref(0)
const selectedTotal = ref(0)
const subtotals = ref([])

const addItem = () => {
  if (items && items.value) {
    items.value.push({
      title: '',
      quantity: 1,
      site: '',
      cashPrice: 0,
      installmentPrice: 0,
      selectedPriceType: 'cash'
    })
    // Scroll automático para o novo item adicionado
    nextTick(() => {
      const container = document.querySelector('.items')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    })
  } else {
    console.error('items is undefined')
  }
}

// Remover o último item da lista
const removeItem = () => {
  items.value.pop()
}

// Atualizar um item na lista pelo índice
const updateItem = (index, newItem) => {
  if (items.value[index]) {
    items.value[index] = { ...items.value[index], ...newItem }
  } else {
    console.error(`Item at index ${index} does not exist`)
  }
}

const updateTotals = (totals) => {
  console.log('updateTotals called with:', totals)
  totalCash.value = isNaN(totals.totalCash) ? 0 : parseFloat(parseFloat(totals.totalCash).toFixed(2))
  totalInstallment.value = isNaN(totals.totalInstallment) ? 0 : parseFloat(parseFloat(totals.totalInstallment).toFixed(2))
  selectedTotal.value = isNaN(totals.selectedTotal) ? 0 : parseFloat(parseFloat(totals.selectedTotal).toFixed(2))
  subtotals.value = Array.isArray(totals.subtotals) ? totals.subtotals : []
  if (Array.isArray(totals.items)) {
    items.value = totals.items
  } else {
    console.error('totals.items is not an array')
  }
}

// Função para lidar com a alteração do tipo de preço selecionado em um item
const handleUpdateSelectedPriceType = ({ index, selectedPriceType }) => {
  if (items.value[index]) {
    items.value[index].selectedPriceType = selectedPriceType
  } else {
    console.error(`Item at index ${index} does not exist`)
  }
}
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: start;
  height: 100vh;
  max-height: 100%;
  width: 100vw;
  max-width: 100%;
  background-color: hsl(0, 0%, 14%);
  box-sizing: border-box;
  flex-wrap: wrap;
  gap: 1em;
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
  overflow: auto;
}

.items-container {
  display: flex;
  flex-direction: column;
  gap: 1em;
  background-color: #1a1a1a;
  padding: 1em;
  border-radius: 0.5rem;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  margin-bottom: 1rem;
  max-width: 31.25rem;
  width: 100%;
  height: 56.33rem;
  max-height: calc(5 * 5.33rem);
  scrollbar-width: none;
  overflow: hidden;
  overflow-y: overlay;
  overflow-x: hidden;
}

.items-container::-webkit-scrollbar {
  display: none;
}

.spacer {
  height: 0.1rem;
}

.left .items {
  max-height: calc(5 * 95px);
  margin-bottom: 1rem;
}

.left .items::-webkit-scrollbar {
  width: 0px;
}

.left .items::-webkit-scrollbar-track {
  background: #444;
  border-radius: 0.2rem;
}

.left .items::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0.2rem;
}

.left .buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.right>* {
  flex: 1;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 100%;
  height: 13rem;
  padding: 1em;
  background-color: #1a1a1a;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  border-radius: 1rem;
  margin-top: auto;
  box-sizing: border-box;
  overflow: hidden;
}

.footer>div {
  flex: 1;
  margin: 0 0.5em;
  overflow: hidden;
}

.footer>div:first-child {
  border-right: 1px solid #646cff;
  padding-right: 0.5em;
}

.footer>div:last-child {
  padding-left: 0.5em;
}

/* Quando a largura da janela do navegador é 600px ou menos */
@media (max-width: 600px) {
  .app {
    flex-direction: column;
    align-items: stretch;
  }

  .left,
  .right {
    width: 100%;
    max-width: 100%;
  }
}
</style>