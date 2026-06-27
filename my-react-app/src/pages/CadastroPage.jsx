import { useState } from "react";
import { useNavigate } from "react-router-dom"; 


function CadastroPage() {

    const navigate = useNavigate();

    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [confirmarSenha, setconfirmarSenha] = useState("");

    const [erros, setErros] = useState({
        nome: "",
        email: "",
        senha:"",
        confirmarSenha:""
    });

    const [sucesso, setSucesso] = useState("");


function validarFormulario() {
    let valido = true;

    let novosErros = {
       nome: "",
       email: "",
       senha:"",
       confirmarSenha:"" 
    };

    if (!nome.trim()) {
        novosErros.nome = "Digite seu nome.";
        valido = false;
    }


    if (!email.trim()) {
        novosErros.email = "Digite seu email.";
        valido = false;    
    } else if (!email.includes("@")) {
        novosErros.email = "Email inválido.";
        valido = false;
    }

    if (!senha.trim()) {
        novosErros.senha = "Digite sua senha.";
        valido = false;
    } else if (senha.length < 6) {
      novosErros.senha = "A senha deve ter pelo menos 6 caracteres.";
      valido = false;  
    }

    if (!confirmarSenha.trim()) {
        novosErros.confirmarSenha = "Digite sua senha.";
        valido = false;
    } else if (confirmarSenha !== senha) {
      novosErros.confirmarSenha = "Senha não encontrada.";
      valido = false;  
    }

    setErros(novosErros);
    return valido;
}  

function criarConta () {
    if (!validarFormulario ())
    {
        setSucesso("");
        return;
    }

    setNome("");
    setEmail("");
    setSenha("");
    setconfirmarSenha("");

    setErros({
        nome: "",
        email: "",
        senha: "",
        confirmarSenha: ""
    });

    setSucesso("Conta criada com sucesso!");
}

    return (
        <div className="w-sreen h-screen flex items-center justify-center bg-sky-900">

            <div className="bg-sky-200 rounded-md w-96 p-6">

                <h1 className="text-2xl font-bold text-center mb-6">
                    Criar Conta
                </h1>

                {sucesso && (
                    <p className="text-green-600 text-center mb-4">
                        {sucesso}
                    </p>
                )}

                <div className="space-y-4">
                    <input 
                    type="text"
                    placeholder="Nome"
                    value={nome} 
                    onChange={(e) => setNome(e.target.value)}
                    className="w-full p-2 rounded border bg-white"
                     />

                    {erros.nome && (
                        <p className="text-red-500 text-sm">
                            {erros.nome}
                        </p>
                    )} 

                     <input 
                    type="email"
                    placeholder="Email"
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full p-2 rounded border bg-white"
                     />

                     {erros.email && (
                        <p className="text-red-500 text-sm">
                            {erros.email}
                        </p>
                    )} 

                     <input 
                    type="password"
                    placeholder="senha"
                    value={senha} 
                    onChange={(e) => setSenha(e.target.value)}
                    className="w-full p-2 rounded border bg-white"
                     />

                     {erros.senha && (
                        <p className="text-red-500 text-sm">
                            {erros.senha}
                        </p>
                    )} 

                     <input 
                    type="password"
                    placeholder="confirmar Senha"
                    value={confirmarSenha} 
                    onChange={(e) => setconfirmarSenha(e.target.value)}
                    className="w-full p-2 rounded border bg-white"
                     />

                     {erros.confirmarSenha && (
                        <p className="text-red-500 text-sm">
                            {erros.confirmarSenha}
                        </p>
                    )} 

                    <button
                    onClick={criarConta}
                    className="w-full bg-slate-300 p-2 rounded border hover:bg-slate-400 transition"
                    >
                        Criar Conta
                    </button> 

                    <button
                    onClick={() => navigate("/")}
                    className="w-full bg-white p-2 rounded border hover:bg-gray-100 transition"
                    >
                        Já possui uma conta? Entrar
                    </button>

                </div>

            </div>
        </div>
    );


    
}

export default CadastroPage;