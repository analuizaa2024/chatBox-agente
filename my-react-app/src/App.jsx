import { useEffect, useState, useRef } from "react";
import ChatBox from "./components/ChatBox";
import ChatInput from "./components/ChatInput";
import { useMediaQuery } from "@mui/material";
import "./App.css";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL;
console.log("API_URL:", API_URL);


function App() {
  const navigate = useNavigate();
  const scrollMensagemRef = useRef(null);
  const [mensagens, setMensagens] = useState([]);
  const [nome, setNome] = useState("");
  const [typing, setTyping] = useState(false);

  const isMobile = useMediaQuery("(max-width:500px)");

  // Carrega o nome do localStorage
  useEffect(() => {
    const usuarioSalvo = localStorage.getItem("usuario");

    if (!usuarioSalvo) {
      navigate("/")
      return;
    }
      const usuario = JSON.parse(usuarioSalvo)
      setNome(usuario.name);
    
  }, []);

  // Busca o histórico no backend
  useEffect(() => {
    if (!nome) return;

    fetch(`${API_URL}/mensagens/allMessages`)
      .then((res) => res.json())
      .then((data) => {
        const msgsDoUsuario = data.filter(
          (msg) => msg.user === nome || msg.to === nome
        );

        setMensagens(
          msgsDoUsuario.sort(
            (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
          )
        );
      })
      .catch((err) => console.error("Erro ao carregar histórico:", err));
  }, [nome]);

  // Scroll automático
  useEffect(() => {
    scrollMensagemRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [mensagens]);

  // Envia mensagem
  async function onclickbutton(textoDigitado) {
    const novaMensagem = {
      user: nome,
      msg: textoDigitado,
      to: "atendente",
    };

    // Mostra a mensagem imediatamente no frontend
    setMensagens((prev) => [...prev, novaMensagem]);

    try {
      // Salva no backend
      await fetch(`${API_URL}/mensagens/allMessages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(novaMensagem),
      });

      // Recarrega todas as mensagens atualizadas
      const res = await fetch(`${API_URL}/mensagens/allMessages`);
      const data = await res.json();

      const msgsDoUsuario = data.filter(
        (msg) => msg.user === nome || msg.to === nome
      );

      setMensagens(
        msgsDoUsuario.sort(
          (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
        )
      );
    } catch (err) {
      console.error("Erro ao enviar mensagem:", err);
    }
  }

  return (
    <div
      className={`w-screen h-screen flex flex-col bg-sky-100 ${
        isMobile ? "p-2" : "p-6"
      }`}
    >
      <ChatBox
        mensagens={mensagens}
        nome={nome}
        typing={typing}
        scrollMensagemRef={scrollMensagemRef}
        isMobile={isMobile}
      />

      <ChatInput onSend={onclickbutton} />
    </div>
  );
}

export default App;