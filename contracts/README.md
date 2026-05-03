# RE-Atlas Type Contracts

Bu klasör tüm tip kontratlarının tek kaynağıdır. Her değişiklik hem `.py` hem `.ts` dosyasına yansıtılmalıdır.

| Tip | schemas.py | schemas.ts | Kullanan Subagentler |
|---|---|---|---|
| `EnergyType` | `Literal["solar","wind","hybrid"]` | union string | Hepsi |
| `ScoreRequest` | Pydantic model | interface | APIWeaver, MapForge |
| `ScoreBreakdown` | Pydantic model | interface | ScoreSmith, APIWeaver, MapForge |
| `ScoreResponse` | Pydantic model | interface | APIWeaver, MapForge |
| `ProvinceScore` | Pydantic model | interface | APIWeaver, MapForge |
| `DistrictScore` | Pydantic model | interface | APIWeaver, MapForge |
| `ForecastPoint` | Pydantic model | interface | ForecastSage, APIWeaver, MapForge |
| `ForecastResponse` | Pydantic model | interface | ForecastSage, APIWeaver, MapForge |
| `MaintenanceWindow` | Pydantic model | interface | ForecastSage, MapForge |
| `FinancialSummary` | Pydantic model | interface | ScoreSmith, MapForge |
| `WeatherSummary` | Pydantic model | interface | APIWeaver, ScoreSmith |
| `Substation` | Pydantic model | interface | ScoreSmith, MapForge |
| `YekaZone` | Pydantic model | interface | ScoreSmith, MapForge |
| `FilterState` | Pydantic model | interface | MapForge |
| `CompareRequest` | Pydantic model | interface | APIWeaver, MapForge |
| `CompareResponse` | Pydantic model | interface | APIWeaver, MapForge |

**Kural:** Bu dosyayı değiştirmeden önce etkilenen tüm subagentleri bildir.
