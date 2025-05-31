import { addMessage } from '@/store/store'
import { useDispatch } from 'react-redux'

const test = async () => {
    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

const sendInput = async (inputData) => {
    const body = {
        input: inputData
    }
    try {
        const response = await fetch('http://localhost:8000/input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data)
        addMessage(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};

export { test, sendInput }
