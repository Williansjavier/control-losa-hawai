import React, { useState } from 'react';
import { 
  Hammer, 
  Layers, 
  Droplet, 
  Clock, 
  Box, 
  Grid, 
  Archive, 
  Truck, 
  Activity, 
  CheckCircle,
  AlertCircle,
  Calendar,
  Construction,
  Info,
  Sparkles,
  FileText,
  ShieldAlert,
  Bot,
  Loader2
} from 'lucide-react';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [reinforcementOption, setReinforcementOption] = useState('A'); // A = Varilla, B = Cercha
  
  // Estados para IA
  const [aiLoading, setAiLoading] = useState(false);
  const [logNotes, setLogNotes] = useState('');
  const [aiReport, setAiReport] = useState('');
  const [safetyAnalysis, setSafetyAnalysis] = useState(null);

  // Datos del proyecto
  const projectData = {
    name: "CLUB HAWAI",
    area: 265,
    type: "Losa Nervada en un Sentido (e=20cm)",
    strength: "f'c = 210 kg/cm²",
    totalDurationEstimada: "15-18 Días Hábiles"
  };

  // Actividades y Tiempos Estimados
  const activities = [
    {
      id: 1,
      title: "Montaje de Encofrado y Apuntalamiento",
      duration: "5 Días",
      status: "Pendiente",
      icon: <Construction className="w-6 h-6" />,
      description: "Nivelación, colocación de parales y tendido de camillas de madera/metal."
    },
    {
      id: 2,
      title: "Armado de Bloques y Acero",
      duration: "4 Días",
      status: "Pendiente",
      icon: <Layers className="w-6 h-6" />,
      description: "Colocación de bloques de anime (15x50x200), armado de nervios y malla electrosoldada."
    },
    {
      id: 3,
      title: "Vaciado de Concreto",
      duration: "1 Día",
      status: "Pendiente",
      icon: <Truck className="w-6 h-6" />,
      description: "Vaciado monolítico con concreto f'c 210 kg/cm², vibrado y regleado."
    },
    {
      id: 4,
      title: "Curado de Concreto",
      duration: "7 Días",
      status: "Pendiente",
      icon: <Droplet className="w-6 h-6" />,
      description: "Riego continuo de agua para garantizar la hidratación y resistencia final."
    }
  ];

  // Materiales Base
  const baseMaterials = [
    { name: "Cemento Gris Portland Tipo I", quantity: 159, unit: "Sacos", icon: <Archive /> },
    { name: "Piedra Picada", quantity: 19, unit: "m³", icon: <Box /> },
    { name: "Arena Lavada", quantity: 8, unit: "m³", icon: <Grid /> },
    { name: "Bloque Anime (15x60x200)", quantity: 175, unit: "Piezas", icon: <Layers /> },
    { name: "Malla Electrosoldada (15x15)", quantity: 4, unit: "Rollos (100m² c/u)", icon: <Grid /> },
  ];

  // --- INTEGRACIÓN GEMINI API ---
  const callGeminiAPI = async (prompt) => {
    setAiLoading(true);
    const apiKey = ""; // La clave se inyecta en tiempo de ejecución
    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }]
          })
        }
      );
      
      if (!response.ok) {
        throw new Error(`Error API: ${response.status}`);
      }

      const data = await response.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "No se pudo generar una respuesta.";
      return text;
    } catch (error) {
      console.error("Error al llamar a Gemini:", error);
      return "Hubo un error al conectar con el asistente de IA. Por favor intenta de nuevo.";
    } finally {
      setAiLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!logNotes.trim()) return;
    const prompt = `Actúa como un Ingeniero Civil Residente experto. Redacta un asiento formal para el CUADERNO DE BITÁCORA (Libro de Obra) para el proyecto "Losa Entrepiso Club Hawai" (265m2).
    
    Usa estas notas crudas del usuario sobre lo que pasó hoy: "${logNotes}".
    
    Estructura la respuesta así:
    1. Encabezado (Fecha, Proyecto).
    2. Resumen de Actividades (Lenguaje técnico formal).
    3. Incidencias/Observaciones.
    4. Conclusión breve.
    Mantén un tono profesional y técnico.`;
    
    const result = await callGeminiAPI(prompt);
    setAiReport(result);
  };

  const handleSafetyAnalysis = async (activityName) => {
    const prompt = `Para la actividad de construcción civil: "${activityName}" en una losa nervada.
    Genera un análisis de seguridad breve con:
    1. Tres (3) Riesgos Críticos específicos.
    2. Lista de EPP (Equipos de Protección Personal) obligatorios.
    3. Una recomendación de seguridad "Regla de Oro".
    Usa formato markdown con viñetas.`;
    
    const result = await callGeminiAPI(prompt);
    setSafetyAnalysis({ activity: activityName, content: result });
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
      
      {/* HEADER / BRANDING */}
      <header className="bg-white border-b border-gray-300 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center gap-2">
               <div className="h-12 w-12 bg-black text-white flex items-center justify-center font-bold text-xl rounded-sm hexagon-mask">
                 HM
               </div>
               <div className="flex flex-col">
                 <h1 className="text-xl font-bold tracking-tight text-gray-900 leading-none">HM RENDERING</h1>
                 <span className="text-sm font-light text-gray-500 tracking-widest">STUDIO 3D</span>
               </div>
            </div>
          </div>
          <div className="text-right hidden md:block">
            <h2 className="text-lg font-bold text-gray-800">{projectData.name}</h2>
            <p className="text-xs text-gray-500 uppercase tracking-wide">Ejecución de Losa Entrepiso</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* KPI CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg p-6 border-l-4 border-black shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 font-medium uppercase">Área Total</p>
                <p className="text-3xl font-bold text-gray-900">{projectData.area} m²</p>
              </div>
              <Grid className="text-gray-300 w-10 h-10" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-6 border-l-4 border-gray-600 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 font-medium uppercase">Tiempo Estimado</p>
                <p className="text-2xl font-bold text-gray-900">~17 Días</p>
              </div>
              <Clock className="text-gray-300 w-10 h-10" />
            </div>
          </div>

          <div className="bg-white rounded-lg p-6 border-l-4 border-gray-400 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 font-medium uppercase">Concreto</p>
                <p className="text-2xl font-bold text-gray-900">210 kg/cm²</p>
              </div>
              <Activity className="text-gray-300 w-10 h-10" />
            </div>
          </div>

           <div className="bg-white rounded-lg p-6 border-l-4 border-gray-200 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 font-medium uppercase">Espesor Losa</p>
                <p className="text-3xl font-bold text-gray-900">20 cm</p>
              </div>
              <Layers className="text-gray-300 w-10 h-10" />
            </div>
          </div>
        </div>

        {/* TABS CONTROLLER */}
        <div className="flex space-x-1 mb-6 bg-gray-200 p-1 rounded-lg w-full md:w-fit overflow-x-auto">
          <button 
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-2 whitespace-nowrap rounded-md text-sm font-medium transition-all ${activeTab === 'overview' ? 'bg-white text-black shadow-sm' : 'text-gray-600 hover:text-black'}`}
          >
            Cronograma
          </button>
          <button 
            onClick={() => setActiveTab('materials')}
            className={`px-6 py-2 whitespace-nowrap rounded-md text-sm font-medium transition-all ${activeTab === 'materials' ? 'bg-white text-black shadow-sm' : 'text-gray-600 hover:text-black'}`}
          >
            Materiales
          </button>
          <button 
            onClick={() => setActiveTab('ai-assistant')}
            className={`px-6 py-2 whitespace-nowrap rounded-md text-sm font-medium transition-all flex items-center ${activeTab === 'ai-assistant' ? 'bg-gradient-to-r from-gray-900 to-gray-700 text-white shadow-sm' : 'text-gray-600 hover:text-black'}`}
          >
            <Sparkles className="w-4 h-4 mr-2" /> Asistente IA
          </button>
        </div>

        {/* CONTENT - OVERVIEW */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <Calendar className="mr-2" /> Ruta de Ejecución
              </h3>
              
              <div className="relative border-l-2 border-gray-300 ml-3 space-y-8 pb-4">
                {activities.map((activity, index) => (
                  <div key={activity.id} className="relative pl-8">
                    {/* Timeline Dot */}
                    <div className="absolute -left-[9px] top-0 bg-white border-2 border-black w-4 h-4 rounded-full"></div>
                    
                    <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow group">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center gap-2">
                          <div className="p-2 bg-gray-100 rounded-md text-gray-700">
                            {activity.icon}
                          </div>
                          <h4 className="text-lg font-bold text-gray-900">{activity.title}</h4>
                        </div>
                        <span className="px-3 py-1 bg-gray-900 text-white text-xs font-bold rounded uppercase">
                          {activity.duration}
                        </span>
                      </div>
                      <p className="text-gray-600 text-sm mb-3 pl-12">{activity.description}</p>
                      
                      {/* Visual Progress Bar (Static representation of weight) */}
                      <div className="pl-12 w-full mb-2">
                        <div className="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                           <div className="h-full bg-gray-400" style={{width: index === 3 ? '100%' : '20%'}}></div>
                        </div>
                      </div>

                      {/* AI Quick Action */}
                      <div className="pl-12 mt-3 pt-3 border-t border-gray-100 hidden group-hover:block transition-all">
                         <button 
                           onClick={() => { setActiveTab('ai-assistant'); handleSafetyAnalysis(activity.title); }}
                           className="text-xs flex items-center text-purple-600 font-medium hover:text-purple-800"
                         >
                           <ShieldAlert className="w-3 h-3 mr-1" /> Analizar Riesgos con IA
                         </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-800 flex items-center">
                <Info className="mr-2" /> Notas Técnicas
              </h3>
              <div className="bg-gray-800 text-white p-6 rounded-lg shadow-lg">
                <h4 className="text-lg font-bold mb-4 border-b border-gray-600 pb-2">Especificaciones</h4>
                <ul className="space-y-4 text-sm text-gray-300">
                  <li className="flex justify-between">
                    <span>Resistencia (f'c):</span>
                    <span className="font-bold text-white">210 kg/cm²</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Acero (fy):</span>
                    <span className="font-bold text-white">4200 kg/cm²</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Recubrimiento Mín:</span>
                    <span className="font-bold text-white">2.00 cm</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Espesor Capa Comp.:</span>
                    <span className="font-bold text-white">5 cm</span>
                  </li>
                </ul>
              </div>

              <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                <h4 className="font-bold text-gray-800 mb-2 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-2" /> Recomendaciones
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-2">
                  <li>Vibrar el concreto con aguja durante el vaciado.</li>
                  <li>Grifar ligeramente varillas en intersecciones viga-columna.</li>
                  <li>Mantener curado húmedo por 7 días mínimo.</li>
                  <li>Notificar al calculista cualquier variación en dimensiones.</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* CONTENT - MATERIALS */}
        {activeTab === 'materials' && (
          <div>
            <div className="flex flex-col md:flex-row justify-between items-end md:items-center mb-6">
               <h3 className="text-xl font-bold text-gray-800 flex items-center mb-4 md:mb-0">
                <Archive className="mr-2" /> Inventario de Materiales
              </h3>
              
              {/* Option Toggle */}
              <div className="bg-white p-1 rounded-lg border border-gray-300 inline-flex">
                 <button 
                  onClick={() => setReinforcementOption('A')}
                  className={`px-4 py-2 text-sm rounded transition-colors ${reinforcementOption === 'A' ? 'bg-black text-white' : 'text-gray-500 hover:bg-gray-100'}`}
                 >
                   Opción A: Cabilla
                 </button>
                 <button 
                  onClick={() => setReinforcementOption('B')}
                  className={`px-4 py-2 text-sm rounded transition-colors ${reinforcementOption === 'B' ? 'bg-black text-white' : 'text-gray-500 hover:bg-gray-100'}`}
                 >
                   Opción B: Cercha
                 </button>
              </div>
            </div>

            {/* Main Materials Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {baseMaterials.map((item, idx) => (
                <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 flex items-center space-x-4">
                  <div className="p-3 bg-gray-100 rounded-full text-gray-800">
                    {item.icon}
                  </div>
                  <div>
                    <p className="text-gray-500 text-xs font-bold uppercase tracking-wider">{item.name}</p>
                    <p className="text-2xl font-bold text-gray-900">{item.quantity} <span className="text-sm font-normal text-gray-500">{item.unit}</span></p>
                  </div>
                </div>
              ))}

              {/* Dynamic Card based on Selection */}
              <div className="bg-gray-900 p-6 rounded-xl shadow-md border border-black flex items-center space-x-4 text-white ring-2 ring-offset-2 ring-gray-900">
                <div className="p-3 bg-gray-700 rounded-full text-white">
                  <CheckCircle />
                </div>
                <div>
                  <p className="text-gray-400 text-xs font-bold uppercase tracking-wider">
                    {reinforcementOption === 'A' ? 'Refuerzo (Varilla 3/8")' : 'Refuerzo (Cercha)'}
                  </p>
                  <p className="text-2xl font-bold text-white">
                    {reinforcementOption === 'A' ? '116' : '58'} 
                    <span className="text-sm font-normal text-gray-400"> Piezas (L=6m)</span>
                  </p>
                </div>
              </div>
            </div>

            {/* Material Summary Table */}
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <h4 className="font-bold text-gray-700">Resumen Total de Requerimientos</h4>
              </div>
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Material</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uso Principal</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Cemento Gris</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Concreto Losa</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">159 Sacos</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Piedra Picada</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Agregado Grueso</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">19 m³</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Arena Lavada</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Agregado Fino</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">8 m³</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Bloques Anime</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Aligeramiento (15x60x200)</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">175 Pzas</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Malla Electrosoldada</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Acero Temperatura (15x15)</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">4 Rollos</td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                       {reinforcementOption === 'A' ? 'Varilla 3/8" (Opción A)' : 'Cercha 15cm (Opción B)'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Refuerzo Nervios</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 text-right">
                       {reinforcementOption === 'A' ? '116 Pzas' : '58 Pzas'}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* CONTENT - AI ASSISTANT */}
        {activeTab === 'ai-assistant' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-fadeIn">
            
            {/* Generador de Reportes */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <div className="bg-gradient-to-r from-gray-900 to-gray-800 px-6 py-4 flex items-center justify-between">
                  <h3 className="text-white font-bold flex items-center">
                    <FileText className="mr-2 text-purple-300" /> Generador de Bitácora
                  </h3>
                  <Sparkles className="text-yellow-400 w-5 h-5" />
                </div>
                <div className="p-6">
                  <p className="text-sm text-gray-500 mb-4">
                    Escribe notas rápidas de lo ocurrido hoy en la obra y la IA redactará un reporte formal técnico.
                  </p>
                  <textarea
                    value={logNotes}
                    onChange={(e) => setLogNotes(e.target.value)}
                    placeholder="Ej: Hoy terminamos de armar el acero de la mitad de la losa. Hubo un retraso de 2 horas por lluvia. Llegaron los sacos de cemento..."
                    className="w-full p-4 border border-gray-300 rounded-lg h-32 mb-4 focus:ring-2 focus:ring-black focus:border-transparent resize-none text-sm"
                  ></textarea>
                  <button
                    onClick={handleGenerateReport}
                    disabled={aiLoading || !logNotes}
                    className="w-full bg-black text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-all flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {aiLoading ? <Loader2 className="animate-spin mr-2" /> : <Sparkles className="mr-2 w-4 h-4" />}
                    {aiLoading ? "Redactando..." : "Generar Reporte Formal"}
                  </button>
                </div>
              </div>

              {aiReport && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 relative">
                  <div className="absolute top-0 left-0 w-1 h-full bg-purple-600 rounded-l-lg"></div>
                  <h4 className="font-bold text-gray-800 mb-4 flex items-center">
                    <Bot className="mr-2 w-5 h-5 text-purple-600" /> Asiento de Bitácora Generado
                  </h4>
                  <div className="prose prose-sm max-w-none text-gray-600 bg-gray-50 p-4 rounded border border-gray-100 whitespace-pre-line font-mono">
                    {aiReport}
                  </div>
                  <div className="mt-4 flex justify-end">
                    <button className="text-xs text-gray-500 hover:text-black font-medium flex items-center" onClick={() => navigator.clipboard.writeText(aiReport)}>
                      Copiar al portapapeles
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Analista de Seguridad y Consultas */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <div className="bg-gray-100 px-6 py-4 border-b border-gray-200">
                   <h3 className="font-bold text-gray-800 flex items-center">
                    <ShieldAlert className="mr-2 text-red-500" /> Seguridad y Riesgos
                  </h3>
                </div>
                <div className="p-6">
                  <p className="text-sm text-gray-600 mb-4">Selecciona una actividad para analizar sus riesgos específicos:</p>
                  <div className="grid grid-cols-2 gap-2 mb-6">
                    {activities.map(act => (
                      <button
                        key={act.id}
                        onClick={() => handleSafetyAnalysis(act.title)}
                        className="text-xs text-left p-2 rounded border border-gray-200 hover:bg-gray-50 hover:border-gray-400 transition-colors truncate"
                      >
                        {act.title}
                      </button>
                    ))}
                  </div>

                  {safetyAnalysis ? (
                    <div className="bg-red-50 border border-red-100 rounded-lg p-5">
                      <h4 className="font-bold text-red-800 mb-2 flex items-center text-sm">
                        <AlertCircle className="w-4 h-4 mr-2" /> Análisis: {safetyAnalysis.activity}
                      </h4>
                      <div className="text-sm text-red-700 whitespace-pre-line leading-relaxed">
                        {safetyAnalysis.content}
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-40 text-gray-400 border-2 border-dashed border-gray-200 rounded-lg">
                      <Bot className="w-8 h-8 mb-2 opacity-20" />
                      <p className="text-sm">Espera análisis de IA...</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;