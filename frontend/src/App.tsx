import { useState, useRef, useEffect } from 'react';
import { UploadCloud, Activity, User, ShieldCheck, CheckCircle2, AlertCircle, Loader2, FileVideo, Search, Filter, Calendar, Trash2, Database, X } from 'lucide-react';
import axios from 'axios';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // Dashboard States
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  // Search States
  const [searchParams, setSearchParams] = useState({ shirt_color: '', gender: '', object_name: 'person' });
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  
  // Image Modal State (Lightbox)
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  // Storage States
  const [jobs, setJobs] = useState<any[]>([]);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setJobId(null);
      setJobStatus(null);
      setProgress(0);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('/api/v1/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setJobId(res.data.id);
      setJobStatus(res.data.status);
    } catch (err) {
      console.error(err);
      alert('Gagal mengupload video. Pastikan backend menyala!');
    } finally {
      setIsUploading(false);
    }
  };

  const fetchJobs = async () => {
    try {
      const res = await axios.get('/api/v1/video-jobs');
      setJobs(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteJob = async (id: string) => {
    if (!confirm('Hapus video dan semua data ekstraksi AI-nya secara permanen?')) return;
    try {
      await axios.delete(`/api/v1/video-jobs/${id}`);
      fetchJobs(); 
      setSearchResults([]); // <-- INI KUNCI RAHASIANYA! Otomatis mengosongkan tab Search!
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (activeTab === 'storage') {
      fetchJobs();
    }
  }, [activeTab]);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    const currentStatus = jobStatus?.toUpperCase();
    
    if (jobId && (currentStatus === 'PENDING' || currentStatus === 'RUNNING')) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`/api/v1/video-jobs/${jobId}`);
          setJobStatus(res.data.status);
          setProgress(res.data.progress);
          
          const fetchedStatus = res.data.status?.toUpperCase();
          if (fetchedStatus === 'COMPLETED' || fetchedStatus === 'FAILED') {
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [jobId, jobStatus]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSearching(true);
    try {
      const params = new URLSearchParams();
      if (searchParams.object_name) params.append('object_name', searchParams.object_name);
      if (searchParams.shirt_color) params.append('shirt_color', searchParams.shirt_color);
      if (searchParams.gender) params.append('gender', searchParams.gender);

      const res = await axios.get(`/api/v1/search?${params.toString()}`);
      setSearchResults(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const displayStatus = jobStatus?.toUpperCase();

  return (
    <div className="min-h-screen bg-background font-sans flex flex-col relative">
      <nav className="bg-surface border-b border-gray-200/50 sticky top-0 z-40 backdrop-blur-md bg-white/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-14 items-center">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 bg-primary rounded-md flex items-center justify-center">
                <ShieldCheck className="text-white w-4 h-4" />
              </div>
              <span className="font-semibold text-base tracking-tight text-primary">
                Vision Intelligence
              </span>
            </div>
            <div className="flex items-center gap-6 text-sm font-medium text-secondary">
              <button onClick={() => setActiveTab('dashboard')} className={`${activeTab === 'dashboard' ? 'text-primary' : 'hover:text-primary'} transition-colors`}>Overview</button>
              <button onClick={() => setActiveTab('search')} className={`${activeTab === 'search' ? 'text-primary' : 'hover:text-primary'} transition-colors`}>Semantic Search</button>
              <button onClick={() => setActiveTab('storage')} className={`${activeTab === 'storage' ? 'text-primary' : 'hover:text-primary'} transition-colors`}>Storage</button>
              <div className="h-4 w-px bg-gray-300"></div>
              <div className="flex items-center gap-2 text-primary">
                <User className="w-4 h-4" />
                <span>Muhammad Ammar Fasya</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full animate-in fade-in duration-500">
        
        {activeTab === 'dashboard' && (
          <div className="animate-in fade-in duration-300">
            <div className="mb-12">
              <h1 className="text-4xl font-bold tracking-tight text-primary mb-3">Video Analysis</h1>
              <p className="text-lg text-secondary font-light">Securely upload footage to automatically track objects and extract semantic attributes.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2 bg-surface rounded-2xl shadow-sm border border-gray-100 p-10 flex flex-col items-center justify-center min-h-[360px] hover:border-gray-300 transition-all group">
                
                <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept="video/mp4,video/quicktime,video/x-msvideo" className="hidden" />

                {!file ? (
                  <>
                    <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-5 group-hover:scale-105 transition-transform duration-300 cursor-pointer" onClick={() => fileInputRef.current?.click()}>
                      <UploadCloud className="w-8 h-8 text-primary" strokeWidth={1.5} />
                    </div>
                    <h3 className="text-xl font-medium mb-2 text-primary">Select Video Footage</h3>
                    <p className="text-secondary text-center max-w-sm mb-8 text-sm">Supports high-resolution MP4, MOV, or AVI formats. Maximum file size is 500MB.</p>
                    <button onClick={() => fileInputRef.current?.click()} className="bg-primary text-white px-7 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors">Browse Files</button>
                  </>
                ) : (
                  <div className="w-full flex flex-col items-center">
                    <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-5">
                      <FileVideo className="w-8 h-8 text-blue-600" strokeWidth={1.5} />
                    </div>
                    <h3 className="text-lg font-medium mb-1 text-primary text-center truncate max-w-xs">{file.name}</h3>
                    <p className="text-secondary text-sm mb-8">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>

                    {!jobId ? (
                      <div className="flex gap-3">
                        <button onClick={() => setFile(null)} disabled={isUploading} className="px-6 py-2.5 rounded-full text-sm font-medium border border-gray-200 text-primary hover:bg-gray-50 transition-colors disabled:opacity-50">Cancel</button>
                        <button onClick={handleUpload} disabled={isUploading} className="bg-primary text-white px-6 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors disabled:opacity-50 flex items-center gap-2">
                          {isUploading && <Loader2 className="w-4 h-4 animate-spin" />}
                          {isUploading ? 'Uploading...' : 'Process Video'}
                        </button>
                      </div>
                    ) : (
                      <div className="w-full flex flex-col items-center">
                        <div className="w-full max-w-md bg-gray-50 rounded-xl p-6 border border-gray-100 mb-6">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm font-medium text-primary flex items-center gap-2">
                              {displayStatus === 'RUNNING' && <Loader2 className="w-4 h-4 animate-spin text-blue-500" />}
                              {displayStatus === 'COMPLETED' && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                              {displayStatus === 'FAILED' && <AlertCircle className="w-4 h-4 text-red-500" />}
                              Status: {displayStatus || 'PENDING'}
                            </span>
                            <span className="text-sm text-secondary font-medium">{progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div className={`h-2 rounded-full transition-all duration-500 ${displayStatus === 'FAILED' ? 'bg-red-500' : displayStatus === 'COMPLETED' ? 'bg-green-500' : 'bg-primary'}`} style={{ width: `${progress}%` }}></div>
                          </div>
                        </div>
                        {displayStatus === 'COMPLETED' && (
                          <button onClick={() => setActiveTab('search')} className="bg-primary text-white px-6 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors flex items-center gap-2">
                            <Search className="w-4 h-4" /> Go to Semantic Search
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div className="bg-surface rounded-2xl shadow-sm border border-gray-100 p-7 flex flex-col">
                <h3 className="text-sm font-semibold mb-6 flex items-center gap-2 text-primary uppercase tracking-wider">
                  <Activity className="w-4 h-4 text-secondary" />
                  System Status
                </h3>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-secondary">AI Processing Engine</span>
                      <span className={`${displayStatus === 'RUNNING' ? 'text-blue-600' : 'text-green-600'} font-medium`}>
                        {displayStatus === 'RUNNING' ? 'Active' : 'Online'}
                      </span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1">
                      <div className={`${displayStatus === 'RUNNING' ? 'bg-blue-500 animate-pulse' : 'bg-green-500'} h-1 rounded-full w-full`}></div>
                    </div>
                  </div>
                  <div className="pt-2 border-t border-gray-50">
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="text-secondary">YOLOv11 Detector</span>
                      <span className="text-primary font-medium">Ready</span>
                    </div>
                  </div>
                  <div className="pt-2 border-t border-gray-50">
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="text-secondary">Ollama Vision Model</span>
                      <span className="text-primary font-medium">Ready</span>
                    </div>
                  </div>
                </div>
                <div className="mt-auto pt-6 border-t border-gray-100">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-secondary">Database Link</span>
                    <span className="flex items-center gap-2 font-medium text-primary">
                      <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                      </span>
                      Connected
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'search' && (
          <div className="animate-in fade-in duration-300">
            <div className="mb-8">
              <h1 className="text-3xl font-bold tracking-tight text-primary mb-2">Semantic Search</h1>
              <p className="text-secondary font-light">Query your processed footage based on AI-extracted attributes.</p>
            </div>

            <div className="bg-surface rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
              <form onSubmit={handleSearch} className="flex flex-wrap items-end gap-4">
                <div className="flex-1 min-w-[200px]">
                  <label className="block text-sm font-medium text-primary mb-1.5">Object Type</label>
                  <input type="text" placeholder="e.g. person, car" value={searchParams.object_name} onChange={(e) => setSearchParams({...searchParams, object_name: e.target.value})} className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                </div>
                <div className="flex-1 min-w-[200px]">
                  <label className="block text-sm font-medium text-primary mb-1.5">Shirt Color</label>
                  <input type="text" placeholder="e.g. red, black" value={searchParams.shirt_color} onChange={(e) => setSearchParams({...searchParams, shirt_color: e.target.value})} className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all" />
                </div>
                <div className="flex-1 min-w-[200px]">
                  <label className="block text-sm font-medium text-primary mb-1.5">Gender</label>
                  <select value={searchParams.gender} onChange={(e) => setSearchParams({...searchParams, gender: e.target.value})} className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all">
                    <option value="">Any</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </div>
                <button type="submit" disabled={isSearching} className="bg-primary text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors h-[38px] flex items-center gap-2">
                  {isSearching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Filter className="w-4 h-4" />}
                  Search
                </button>
              </form>
            </div>

            <div className="bg-surface rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50/50 border-b border-gray-100">
                  <tr>
                    <th className="px-6 py-4 font-medium text-secondary">Snapshot</th>
                    <th className="px-6 py-4 font-medium text-secondary">Track ID</th>
                    <th className="px-6 py-4 font-medium text-secondary">Object</th>
                    <th className="px-6 py-4 font-medium text-secondary">Attributes Found</th>
                    <th className="px-6 py-4 font-medium text-secondary">Date & Source</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {searchResults.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-secondary">
                        No matches found. Try adjusting your filters.
                      </td>
                    </tr>
                  ) : (
                    searchResults.map((res: any, idx: number) => (
                      <tr key={idx} className="hover:bg-gray-50/50 transition-colors">
                        <td className="px-6 py-4">
                          <div 
                            className="w-14 h-14 rounded-md overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center cursor-pointer group"
                            onClick={() => setSelectedImage(`/${res.crop_path}`)}
                            title="Click to enlarge"
                          >
                            <img 
                              src={`/${res.crop_path}`} 
                              alt="snapshot" 
                              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" 
                            />
                          </div>
                        </td>
                        <td className="px-6 py-4 font-medium">#{res.track_id}</td>
                        <td className="px-6 py-4 capitalize">{res.attributes.object || '-'}</td>
                        <td className="px-6 py-4">
                          <div className="flex flex-wrap gap-2">
                            {res.attributes.shirt_color && <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs border border-gray-200/60">Shirt: {res.attributes.shirt_color}</span>}
                            {res.attributes.gender && <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs border border-gray-200/60">Gender: {res.attributes.gender}</span>}
                            {res.attributes.pants_color && <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs border border-gray-200/60">Pants: {res.attributes.pants_color}</span>}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex flex-col">
                            <span className="font-medium text-primary flex items-center gap-1.5">
                              <Calendar className="w-3.5 h-3.5 text-secondary" /> 
                              {new Date(res.created_at).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}
                            </span>
                            <span className="text-xs text-secondary mt-1.5 flex items-center gap-1.5">
                               <FileVideo className="w-3.5 h-3.5" /> 
                               Vid: {res.video_job_id.substring(0, 8)} • {res.timestamp_seconds.toFixed(1)}s
                            </span>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'storage' && (
          <div className="animate-in fade-in duration-300">
            <div className="mb-8">
              <h1 className="text-3xl font-bold tracking-tight text-primary mb-2 flex items-center gap-3">
                <Database className="w-7 h-7 text-primary" /> Data Storage
              </h1>
              <p className="text-secondary font-light">Manage your uploaded video footage and AI detection records.</p>
            </div>
            
            <div className="bg-surface rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50/50 border-b border-gray-100">
                  <tr>
                    <th className="px-6 py-4 font-medium text-secondary">Filename</th>
                    <th className="px-6 py-4 font-medium text-secondary">Status</th>
                    <th className="px-6 py-4 font-medium text-secondary">Upload Date</th>
                    <th className="px-6 py-4 font-medium text-secondary text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {jobs.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-12 text-center text-secondary">
                        Storage is empty. No video data found.
                      </td>
                    </tr>
                  ) : (
                    jobs.map((j: any, idx: number) => (
                      <tr key={idx} className="hover:bg-gray-50/50 transition-colors group">
                        <td className="px-6 py-4 font-medium truncate max-w-xs">{j.filename}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-1 rounded text-xs font-medium border ${j.status === 'COMPLETED' ? 'bg-green-50 text-green-700 border-green-200/60' : j.status === 'FAILED' ? 'bg-red-50 text-red-700 border-red-200/60' : 'bg-blue-50 text-blue-700 border-blue-200/60'}`}>
                            {j.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-secondary">
                          {new Date(j.created_at).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button 
                            onClick={() => handleDeleteJob(j.id)} 
                            className="text-gray-400 hover:text-red-600 transition-colors p-2 rounded-md hover:bg-red-50 opacity-0 group-hover:opacity-100"
                            title="Delete Video Data"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Image Modal (Lightbox) */}
      {selectedImage && (
        <div 
          className="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/80 backdrop-blur-sm p-4 animate-in fade-in duration-200"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative max-w-4xl max-h-[90vh] flex items-center justify-center animate-in zoom-in-95 duration-200">
            <button 
              className="absolute -top-4 -right-4 md:-top-6 md:-right-6 bg-white text-gray-900 p-2 rounded-full shadow-lg hover:bg-gray-100 transition-colors z-10"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedImage(null);
              }}
            >
              <X className="w-5 h-5" />
            </button>
            <img 
              src={selectedImage} 
              alt="Enlarged snapshot" 
              className="max-w-full max-h-[85vh] object-contain rounded-xl shadow-2xl border border-gray-700/50" 
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        </div>
      )}
    </div>
  );
}
