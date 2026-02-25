from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models.usuario_model import UsuarioModel
from models.vwapriori_model import VwAprioriModel
from schemas.vwapriori_schema import VwAprioriSchema
from core.deps import get_session_JEDi, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# GET Logado
@router.get('/', response_model=List[VwAprioriSchema])
async def get_rules(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    async with db as session:
        query = select(VwAprioriModel)
        result = await session.execute(query)
        apriori: List[VwAprioriSchema] = result.scalars().unique().all()
        
        return apriori
