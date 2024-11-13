import { useState, useEffect } from 'react'
import axios from 'axios'
import { Container, TextField, Button, List, ListItem, ListItemText, ListItemButton, ListItemIcon } from '@mui/material'

function App() {
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState('')

  // Fetch todos
  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      const response = await axios.get('http://localhost:8000/todos')
      setTodos(response.data)
    } catch (error) {
      console.error('Error fetching todos:', error)
    }
  }

  // Create todo
  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await axios.post('http://localhost:8000/todos', {
        title: newTodo,
        completed: false
      })
      setNewTodo('')
      fetchTodos()
    } catch (error) {
      console.error('Error creating todo:', error)
    }
  }

  // Toggle todo completion
  const toggleTodo = async (id, completed) => {
    try {
      await axios.put(`http://localhost:8000/todos/${id}`, {
        completed: !completed
      })
      fetchTodos()
    } catch (error) {
      console.error('Error updating todo:', error)
    }
  }

  // Delete todo
  const deleteTodo = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/todos/${id}`)
      fetchTodos()
    } catch (error) {
      console.error('Error deleting todo:', error)
    }
  }

  return (
    <Container maxWidth="sm" sx={{
      bgcolor: 'white',
      minHeight: '100vh', // Full height
      padding: 3,        // Add some padding
      boxShadow: 1
    }}>
      <h1 style={{ color: 'black' }}>Todo App</h1>

      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Add a new todo"
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary">
          Add Todo
        </Button>
      </form>

      <List>
        {todos.map((todo) => (
          <ListItem key={todo.id} disablePadding>
            <ListItemButton onClick={() => toggleTodo(todo.id, todo.completed)}>
              <ListItemText
                primary={todo.title}
                style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
              />
              <ListItemIcon sx={{ minWidth: 'auto' }}>
                <IconButton edge="end" onClick={(e) => {
                  e.stopPropagation();
                  deleteTodo(todo.id);
                }}>
                  🗑️
                </IconButton>
              </ListItemIcon>
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Container>
  )
}

export default App 