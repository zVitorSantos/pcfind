<!-- Items.vue -->
<template>
  <div v-if="errorMessage" class="error-notification">
    {{ errorMessage }}
  </div>
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
        <input type="text" v-model="siteDisplay" @focus="siteFocused = true" @blur="siteFocused = false" />
      </div>
      <div class="bottom-row">
        <input type="text" v-model="item.cashPrice" placeholder="Valor à vista" />
        <input type="text" v-model="item.installmentPrice" placeholder="Valor parcelado" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue'
import axios from 'axios';

const props = defineProps({
  modelValue: Object
})

const emit = defineEmits(['update:modelValue'])

const item = ref(props.modelValue || {
  title: '',
  quantity: 1,
  site: '',
  siteName: '',
  cashPrice: 0,
  installmentPrice: 0
})

const manualEntry = ref(false)
const errorMessage = ref('')

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

const getHostName = (url) => {
  try {
    const urlObj = new URL(url);
    const hostName = urlObj.hostname;
    // Remove 'www.' if present
    const name = hostName.startsWith('www.') ? hostName.slice(4) : hostName;
    // Split the host name into parts
    const parts = name.split('.');
    // Find the first part that is more than 2 characters long
    const shortName = parts.find(part => part.length > 2) || parts[0];
    // Capitalize the first letter
    return shortName.charAt(0).toUpperCase() + shortName.slice(1);
  } catch (e) {
    console.error(e);
    return '';
  }
}

const siteFocused = ref(false)

const siteDisplay = computed({
  get: () => siteFocused.value ? item.value.site : getHostName(item.value.site),
  set: (newValue) => {
    item.value.site = newValue;
    item.value.siteName = getHostName(item.value.site);
  }
});

const searchItem = async () => {
  if (!item.value.site) {
    console.error('Site não especificado');
    return;
  }

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
    console.error('Erro na busca:', error);

    if (axios.isAxiosError(error) && error.response && error.response.status === 400) {
      // Exibir mensagem de erro específica retornada pelo servidor
      const errorMessageText = error.response.data.error || 'Erro de requisição inválida';
      errorMessage.value = errorMessageText;
    } else {
      // Exibir mensagem de erro genérica para outros tipos de erro
      errorMessage.value = 'Erro ao processar a requisição.';
    }

    // Limpar a mensagem de erro após um intervalo de tempo (opcional)
    setTimeout(() => {
      errorMessage.value = '';
    }, 5000);
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
  padding-right: 40px;
  /* Increase padding to prevent text overlap */
  text-align: left;
  width: 100%;
}

.search-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  color: rgba(255, 255, 255, 0.87);
  cursor: pointer;
  padding: 0.5rem;
  width: 30px;
  /* Adjust width */
  height: 30px;
  /* Adjust height */
  text-align: center;
  font-size: 1rem;
  /* Adjust font size */
}

.error-notification {
  position: fixed;
  top: 1%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ac2020;
  color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  border: 1px solid #646cff;
  font-weight: bold;
}
</style>