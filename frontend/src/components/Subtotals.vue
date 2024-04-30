<!-- Subtotals.vue -->
<template>
  <div class="subtotals">
    <h2>Subtotal</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Componente</th>
            <th>À vista</th>
            <th>Parcelado</th>
            <th>R$</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(subtotal, index) in subtotals" :key="index">
            <td>{{ `${subtotal.component} ${subtotal.quantity > 1 ? `${subtotal.quantity}x` : ''}` }}</td>
            <td>{{ subtotal.cashPrice }}</td>
            <td>{{ subtotal.installmentPrice }}</td>
            <td>
              <select v-model="subtotal.selectedPriceType">
                <option value="cash">À vista</option>
                <option value="installment">Parcelado</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps({
  items: Array
})

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

const subtotals = computed(() => {
  return props.items.map(item => {
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
.subtotals {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  margin: 0 auto;
}

.subtotals h2 {
  padding-top: 0;
  padding-bottom: 0.5rem;
  margin-top: 0;
  margin-bottom: 0;
}

.table-container {
  height: 350px;
  max-height: calc(5 * 70px);
  width: 100%;
  max-width: 100%;
  overflow: overlay;
  scrollbar-width: none;
}

/* Para navegadores baseados em WebKit */
.table-container::-webkit-scrollbar {
  display: none;
}

.subtotals .table-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  gap: 1em;
  background-color: #1a1a1a;
  padding: 1em;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.87);
  border: 1px solid #646cff;
  margin-bottom: 1em;
  max-height: calc(5 * 70px);
}

.subtotals table {
  width: 100%;
  border-collapse: collapse;
}

.subtotals th,
.subtotals td {
  border: 1px solid #ddd;
  padding: 8px;
}

.subtotals th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #242424;
  color: white;
}

.subtotals th:nth-child(4),
.subtotals td:nth-child(4) {
  width: 100px;
}
</style>