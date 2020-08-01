# Importação do Pymem, usado para ler e escrever na memória
import pymem
import pymem.process

# Definição dos offsets do jogo
dwEntityList = (0x4D534EC)
dwGlowObjectManager = (0x529B3C8)
m_iGlowIndex = (0xA438)
m_iTeamNum = (0xF4)

# Função principal
def main():
    pm = pymem.Pymem("csgo.exe") # Pega o processo do CS:GO
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # Pega o endereço base da client.dll

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager) # Lê o endereço do dwGlowObjectManager (dwGlowObjectManager pode ser considerado como o controlador do Glow do jogo)

        for i in range(1, 64):  # Para cada entidade (Entidade pode ser entendida como Player / Jogador, mas não se limita a ele.)
            entity = pm.read_int(client + dwEntityList + i * 0x10) # Lê o endereço base da entidade atual

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum) # Lê o endereço m_iTeamNum da entidade atual (m_iTeamNum define qual o seu Team / Equipe.
                entity_glow = pm.read_int(entity + m_iGlowIndex) # Lê o endereço m_iGlowIndex da entidade (m_iGlowIndex, como o nome sugere é o Index da struct Glow)

                if entity_team_id == 2:  # Se a entidade atual for Terroristas
					# Vamos escrever na struct glow da nossa entidade, para definirmos a cor, opacidade e setarmos como True na memória, para qu seja exibida
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # Red 	 / Vermelho 
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # Green  / Verde
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # Blue	 / Azul
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha  / Opacidade
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable / Ativar

                elif entity_team_id == 3:  # Se a entidade atual for Contra-terroristas
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # Red 	 / Vermelho
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # Green  / Verde
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # Blue	 / Azul
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha  / Opacidade
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable / Ativar


if __name__ == '__main__':
    main() #Roda a função main se executado o arquivo diretamente