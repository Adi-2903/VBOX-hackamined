/**
 * Episense API Client
 * Types match the BACKEND_INTEGRATION_GUIDE.md output format exactly.
 */

const API_BASE = "http://localhost:8000/api/v1";

// ─── Types matching backend schemas (BACKEND_INTEGRATION_GUIDE.md) ───

// GenAI output
export interface GeneratedEpisode {
    episode_number: number;
    title: string;
    hook: string;
    story: string;
    cliffhanger: string;
    text_overlays_suggestions: string[];
}

export interface GeneratedSeries {
    category: string;
    direction: string;
    hook: string;
    episodes: GeneratedEpisode[];
}

// ML Analysis — Features
export interface SemanticFeatures {
    hook_strength: number;
    conflict_score: number;
    cliffhanger_score: number;
    hook_reason: string;
    conflict_reason: string;
    cliffhanger_reason: string;
}

export interface EmotionalArc {
    emotion_variance: number;
    emotion_peak: number;
    climax_position: number;
    arc_shape: string;
    reason: string;
}

export interface NarrativeStructure {
    structure_quality: string;
    hook_position_score: number;
    conflict_density: number;
    twist_position_score: number;
    reason: string;
}

export interface DropoffSegment {
    label: string;
    dropoff_risk: number;
    engagement_score: number;
}

export interface DropoffPrediction {
    overall_dropoff_risk: number;
    high_risk_segments: number[];
    segments: DropoffSegment[];
    reason: string;
}

export interface Features {
    semantic_features: SemanticFeatures;
    emotional_arc: EmotionalArc;
    narrative_structure: NarrativeStructure;
    dropoff_prediction: DropoffPrediction;
}

// ML Analysis — Retention
export interface SegmentRisk {
    risk: number;
    label: string;
}

export interface Recommendation {
    area: string;
    priority: string;
    suggestion: string;
}

export interface Retention {
    risk_score: number;
    risk_level: string;
    segment_risks: Record<string, SegmentRisk>;
    reason: string;
    recommendations: Recommendation[];
}

// ML Analysis — Cliffhanger
export interface CliffhangerComponents {
    surprise: number;
    emotion_spike: number;
    conflict_signal: number;
    keyword_boost: number;
}

export interface Cliffhanger {
    cliffhanger_score: number;
    strength: string;
    components: CliffhangerComponents;
    category: string;
    keywords_found: Record<string, string[]>;
    reason: string;
}

// ML Analysis — Summary
export interface AnalysisSummary {
    overall_score: number;
    engagement_level: string;
    key_strengths: string[];
    key_weaknesses: string[];
}

// Complete Episode Analysis (output of analyze_episode_v2)
export interface EpisodeAnalysis {
    category: string;
    features: Features;
    retention: Retention;
    cliffhanger: Cliffhanger;
    summary: AnalysisSummary;
}

// Episode with metadata (in series context)
export interface EpisodeAnalysisWithMeta {
    episode_number: number;
    title: string;
    analysis: EpisodeAnalysis;
}

// Series Analysis
export interface SeriesInsights {
    avg_overall_score: number;
    trend: string;
    consistency_score: number;
    weakest_episode: number;
    strongest_episode: number;
}

export interface SeriesAnalysis {
    episodes: EpisodeAnalysisWithMeta[];
    series_insights: SeriesInsights;
}

// Project
export interface ProjectResponse {
    id: string;
    title: string;
    concept: string;
    genres: string[];
    generated_series: GeneratedSeries | null;
    analysis: SeriesAnalysis | null;
    status: string;
    created_at: string;
    episode_count: number;
    overall_score: number | null;
}

// Direction suggestions (GenAI step 1)
export interface DirectionSuggestion {
    direction_name: string;
    category: string;
    why_it_fits: string;
}

export interface DirectionsResponse {
    suggested_directions: DirectionSuggestion[];
}

// ─── API Functions ───

export async function getDirections(concept: string): Promise<DirectionsResponse> {
    const res = await fetch(`${API_BASE}/engine/directions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept }),
    });
    if (!res.ok) throw new Error(`Directions failed: ${res.statusText}`);
    return res.json();
}

export async function generateSeries(
    concept: string,
    numEpisodes: number,
    genres: string[],
    audience: string = "",
    direction: string = ""
): Promise<GeneratedSeries> {
    const res = await fetch(`${API_BASE}/engine/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept, num_episodes: numEpisodes, genres, audience, direction }),
    });
    if (!res.ok) throw new Error(`Generate failed: ${res.statusText}`);
    return res.json();
}

export async function analyzeEpisode(text: string, category?: string): Promise<EpisodeAnalysis> {
    const res = await fetch(`${API_BASE}/engine/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, category }),
    });
    if (!res.ok) throw new Error(`Analysis failed: ${res.statusText}`);
    return res.json();
}

export async function analyzeSeries(episodes: GeneratedEpisode[], category?: string): Promise<SeriesAnalysis> {
    const res = await fetch(`${API_BASE}/engine/analyze-series`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ episodes, category }),
    });
    if (!res.ok) throw new Error(`Series analysis failed: ${res.statusText}`);
    return res.json();
}

export async function listProjects(): Promise<ProjectResponse[]> {
    const res = await fetch(`${API_BASE}/projects`);
    if (!res.ok) throw new Error(`Listing projects failed: ${res.statusText}`);
    return res.json();
}

export async function getProject(id: string): Promise<ProjectResponse> {
    const res = await fetch(`${API_BASE}/projects/${id}`);
    if (!res.ok) throw new Error(`Get project failed: ${res.statusText}`);
    return res.json();
}

export async function createProject(data: {
    title: string;
    concept: string;
    genres: string[];
    generated_series: GeneratedSeries | null;
    analysis: SeriesAnalysis | null;
}): Promise<ProjectResponse> {
    const res = await fetch(`${API_BASE}/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`Create project failed: ${res.statusText}`);
    return res.json();
}

export async function deleteProject(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/projects/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`Delete project failed: ${res.statusText}`);
}
