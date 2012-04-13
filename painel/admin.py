#!/bin/env python
# -*- coding: utf-8 -*-

## [Ficha]##################################################
#	                                                   #
#  Nome: Modulo Admin				           #
#                                                          #
#  Escrito por: Alisson Barbosa Ferreira                   #
#                                                          #
#  Criado em: 10/03/2012			           #
#						           #
#  Ultima atualizacao: 10/03/2012		           #
#						           #
#  [Descricao]##############################################
#					                   #
#  Arquivo que contem as classes que serão adicionadas     #
#  no admin padrão do djando.                              #
#					                   #
############################################################        


from django.contrib             import admin


from models             import Telefones, Contatos, Categorias, Estados, Cidades, \
                               DadosWeb, TelefonesUteis, Pesquisas

################################################################################
#                                                                              #
#                     CLASSE AdminContatos                                     #
#                                                                              #
################################################################################

class TelefonesInline(admin.TabularInline):
    model = Telefones

class DadosWebInline(admin.TabularInline):
    model = DadosWeb

def excluir_contato_selecionado(modeladmin, request, queryset):    
    queryset.update(status=2)


class AdminContatos(admin.ModelAdmin):
    exclude      = ('auth_user','publicidade','status')
    list_display = ('nome','cpf_cnpj','endereco','categorias','cidades','aprovacao')
    list_filter  = ('status',)
    
    actions      = [excluir_contato_selecionado,]
    inlines      = [TelefonesInline,DadosWebInline,]

    
    def queryset(self, request):
        if (request.user.is_superuser == True):
            contatos = super(AdminContatos, self).queryset(request).all()
        else:
            contatos = super(AdminContatos, self).queryset(request).filter(auth_user=request.user.id).exclude(status=2)

        return contatos

    # Salva o id do usuario que cadastrou o telefone
    def save_model(self, request, obj, form, change):
        super(AdminContatos, self).save_model(request, obj, form, change)
	obj.auth_user  = request.user        
        obj.save()


################################################################################
#                                                                              #
#                     CLASSE AdminContatos                                     #
#                                                                              #
################################################################################

class AdminPesquisas(admin.ModelAdmin):
    list_display = ('termo','data','ocorrencia','obteve_sucesso')
    list_filter  = ('exito',)

################################################################################
#                                                                              #
#                            Regitrar classes no admin                         #
#                                                                              #
################################################################################

admin.site.register(Contatos,AdminContatos)
admin.site.register(Pesquisas,AdminPesquisas)

admin.site.register(Categorias)
admin.site.register(TelefonesUteis)
