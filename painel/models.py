#!/bin/env python
# -*- coding: utf-8 -*-

## [Ficha]##################################################
#	                                                   #
#  Nome: Modulo Models				           #
#                                                          #
#  Escrito por: Alisson Barbosa Ferreira                   #
#                                                          #
#  Criado em: 16/02/2012			           #
#						           #
#  Ultima atualizacao: 19/02/2012		           #
#						           #
#  [Descricao]##############################################
#					                   #
#  Arquivo que contem as classes da aplicação de           #
#  alocação de recursos                                    #
#					                   #
############################################################

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User
            

################################################################################
#                                                                              #
#                           CLASSE CATEGORIAS                                  #
#                                                                              #
################################################################################

class Categorias(models.Model):
    class Meta:        
        db_table = 'categorias'        
        verbose_name_plural = ugettext_lazy('Categorias')
        verbose_name        = ugettext_lazy('Categoria')

    nome = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.nome

################################################################################
#                                                                              #
#                           CLASSE ESTADOS                                     #
#                                                                              #
################################################################################

class Estados(models.Model):
    class Meta:
        db_table = u'estados'
        verbose_name_plural = ugettext_lazy('Estados')
        verbose_name        = ugettext_lazy('Estado')

    
    uf      = models.CharField(max_length=30)
    nome    = models.CharField(max_length=60)

    def __unicode__(self):
        return self.nome

################################################################################
#                                                                              #
#                           CLASSE CIDADES                                     #
#                                                                              #
################################################################################

class Cidades(models.Model):
    class Meta:
        ordering = ('id', )
        db_table = 'cidades'
        verbose_name_plural = ugettext_lazy('Cidades')
        verbose_name        = ugettext_lazy('Cidades')

    estado  = models.ForeignKey('Estados')
    uf      = models.CharField(max_length=4, blank=False)
    nome    = models.CharField(max_length=50, blank=False)
    status  = models.IntegerField(max_length=1)

    def __unicode__(self):
        return self.nome

    
################################################################################
#                                                                              #
#                           CLASSE CONTATOS                                    #
#                                                                              #
################################################################################

class Contatos(models.Model):
    class Meta:
        ordering = ('id', )
        db_table = 'contatos'
        verbose_name_plural = ugettext_lazy('Contatos')
        verbose_name        = ugettext_lazy('Contatos')

    nome            = models.CharField('Nome', max_length=100, blank=False)
    cpf_cnpj        = models.CharField('CNPJ', max_length=15)
    endereco        = models.CharField('Endereço', max_length=100, blank=False)
    categorias      = models.ForeignKey('categorias')
    img             = models.ImageField(null=True, blank=True, upload_to='galeria/original', )
    data_alter      = models.DateTimeField(auto_now=True, auto_now_add=True,blank=False)
    descricao       = models.TextField('Endereço', blank=False)
    cidades         = models.ForeignKey('Cidades')
    auth_user       = models.ForeignKey(User)
    publicidade     = models.IntegerField(default=0,max_length=1)
    status          = models.IntegerField(default=0,max_length=1)

    def aprovacao(self):
        if (self.status == 0):
            return u'aguardando aprovação'
        elif (self.status == 1):
            return u'aprovado'
        else:
            return u'excluido'


    def __unicode__(self):
        return self.nome


################################################################################
#                                                                              #
#                           CLASSE TELEFONES                                   #
#                                                                              #
################################################################################

class Telefones(models.Model):
    class Meta:
        ordering = ('id', )    	
        db_table = 'telefones'
        verbose_name_plural = ugettext_lazy('Telefones')
        verbose_name        = ugettext_lazy('Telefones')
        
    
    ddd          = models.IntegerField('DDD', max_length=3)
    numero       = models.CharField('Número', max_length=15)
    contatos     = models.ForeignKey('Contatos')

    def __unicode__(self):
        return '(%s) %s' % (self.ddd, self.numero)

################################################################################
#                                                                              #
#                           CLASSE DADOS WEB                                   #
#                                                                              #
################################################################################

class DadosWeb(models.Model):
    class Meta:
        db_table = u'dados_web'
        verbose_name_plural = ugettext_lazy('Dados Web')
        verbose_name        = ugettext_lazy('Dados Web')

    dado        = models.CharField(max_length=450)
    tipo        = models.CharField(max_length=15)
    contato     = models.ForeignKey('Contatos')

    def __unicode__(self):
        return self.dado


################################################################################
#                                                                              #
#                           CLASSE TELEFONES UTEIS                             #
#                                                                              #
################################################################################


class TelefonesUteis(models.Model):
    class Meta:
        db_table = u'telefones_uteis'
        verbose_name_plural = ugettext_lazy('Telefones Uteis')
        verbose_name        = ugettext_lazy('Telefones Uteis')
        
    nome        = models.CharField(max_length=180)
    telefone    = models.CharField(max_length=60)
    local       = models.ForeignKey('Cidades')

    def __unicode__(self):
        return self.nome


################################################################################
#                                                                              #
#                           CLASSE PESQUISAS                                   #
#                                                                              #
################################################################################


class Pesquisas(models.Model):
    class Meta:
        db_table = u'pesquisas'
        verbose_name_plural = ugettext_lazy('Pesquisas')
        verbose_name        = ugettext_lazy('Pesquisa')

    
    data        = models.DateTimeField('Quando foi pesquisado',auto_now=True, auto_now_add=True,blank=False)
    termo       = models.TextField('Termo pesquisado',blank=False)
    ocorrencia  = models.IntegerField(u'Nº de ocorrências',max_length=3,blank=False)
    exito       = models.IntegerField(max_length=1,blank=False)

    def obteve_sucesso(self):
        if(self.exito == 0):
            return u'Não'
        else:
            return u'Sim'

    def __unicode__(self):
        return self.termo